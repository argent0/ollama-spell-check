#!/usr/bin/env python3
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
        next_lines = list(itertools.islice(lines, 0, 5))

        if not next_lines:
            break

        prompt = [
                "You are a highly intelligent spell checker and grammar assistant. Your primary goal is to identify and correct spelling errors, grammatical mistakes, and punctuation problems in text input.",
                "Only output the corrected text. Do not include any other information in the output.",
                ]

        closer = [
                ]

        corrected = client.query(prompt, closer, next_lines)

        print(corrected)

        if sys.stdin.isatty() or sys.stdin.buffer.peek():
            break

if __name__ == '__main__':
    main()
