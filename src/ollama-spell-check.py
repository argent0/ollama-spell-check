"""
This script uses the OLLama API to correct spelling mistakes in a text.
"""
import sys
import logging
import itertools
import requests

class OLLamaClient:
    """
    A client for the OLLama API.

    The API has no authentication.

    """

    def __init__(self, base_url, model, timeout):
        self.base_url = base_url
        self.model = model
        self.timeout = timeout

    def query(self, prompt_lines, closer_lines, lines):
        """
        Query the OLLama API with a list of lines.
        """
        url = self.base_url + '/api/chat'

        response = requests.post(
                url,
                headers={'Content-Type': 'application/json'},
                json={
                    'model': self.model,
                    'stream': False,
                    'messages': [
                        {
                            'role': 'system',
                            'content': prompt
                        } for prompt in prompt_lines
                    ] + [
                        {
                            'role': 'user',
                            'content': line
                        }
                        for line in lines
                    ] + [
                        {
                            'role': 'system',
                            'content': closer
                        } for closer in closer_lines
                    ]
                },
                timeout=self.timeout
                )

        response.raise_for_status()

        return response.json()['message']['content']


def main():
    client = OLLamaClient(
            base_url='http://localhost:11434',
            model='llama3',
            timeout=10
            )

    lines = sys.stdin

    while True:
        part = itertools.islice(lines, 0, 5)

        part_lines = [line.strip() for line in part if line.strip()]

        if len(part_lines) == 0:
            break

        prompt = [
                "Correct any spelling mistakes in the following text:",
                ]

        closer = [
                "Only output the corrected text.",
                ]


        corrected = client.query(prompt, closer, part_lines)

        print(corrected)

if __name__ == '__main__':
    main()
