#!/usr/bin/python3
"""
Cheers https://github.com/elastic/chatgpt-log-analysis/blob/main/app.py
"""
import os
import sys
import openai
import requests
from copr.v3 import Client

from pprint import pprint

openai.api_key = os.environ["OPEN_API_TOKEN"]


def get_build_logs(build_id):
    """ provide build logs for given failed Copr build as text """
    client = Client.create_from_config_file()

    build = client.build_proxy.get(build_id)

    owner = build['ownername']
    project_name = build['projectname']
    pkg = build['source_package']['name']

    if build['source_package']['name'] is None:
        # srpm failed
        chroot = "srpm-builds"
    else:
        for chroot in build['chroots']:
            build_chroot = client.build_chroot_proxy.get(build_id, chroot)
            if build_chroot['state'] == 'failed':
                break
        else:
            return None

    pkg = "" if chroot == "srpm-builds" else f"-{pkg}"
    logs_url = (
        "https://download.copr.fedorainfracloud.org/"
        f"results/{owner}/{project_name}/{chroot}/"
        f"{build_id:08d}{pkg}/builder-live.log"
    )
    return requests.get(logs_url).text


def get_logs_snippet(logs):
    """
    This function is a stub. As LLMs limit input size, we need to strip the logs from useless information.

    Right now we just naively take last 4k info.

    This function should be much more sophisticated.

    :param logs: logs as text
    :return: subset of the logs as text
    """
    return logs[-4096:]


def prompt_gpt(build_id):
    # OpenAI's docs
    # What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random,
    # while lower values like 0.2 will make it more focused and deterministic.
    # We generally recommend altering this or top_p but not both.
    temperature = 0.5  # defaults to 1

    # OpenAI's docs
    # An alternative to sampling with temperature, called nucleus sampling, where the model considers the results
    # of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability
    # mass are considered. We generally recommend altering this or temperature but not both.
    top_p = 1  # defaults to 1

    logs = get_logs_snippet(get_build_logs(build_id))
    print(f"{logs}\n\n")
    # TODO: trick GPT to output JSON and process it
    # "Output in this JSON format: {\"short_summary\": \"<TBD>\", \"steps_to_fix\": [\"<step1>\", \"step2>\"]}. " +
    prompt = (
        "The RPM build process failed and you need to fix it. " +
        "Please review the logs messages below, explain the root cause for the error and "
        "how it should fixed in the most optimal way. " +
        "The logs start here.\n" +
        logs
    )

    analysis=[{"role": "system", "content": "You are an RPM Package Maintainer and an upstream developer."
                                            " You are responsible for RPM builds to successfully complete."},
              {"role": "user", "content": prompt}]
    analysis_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # TODO we want GPT4!!!!!!
        messages=analysis,
        temperature=temperature,
        top_p=top_p,
    )
    return analysis_response

try:
    build_id = sys.argv[1]
except IndexError:
    print(f"usage: {sys.argv[0]} COPR_BUILD_ID\n\n"
          "  This program requires only a single argument: Copr build ID", file=sys.stderr)
    sys.exit(3)

out = prompt_gpt(int(build_id))
pprint(out)

print(out["choices"][0]["message"]["content"])