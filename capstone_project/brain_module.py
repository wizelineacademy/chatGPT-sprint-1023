#!/usr/bin/env python3

import os
from dotenv import load_dotenv
from openai import OpenAI

class ChatGPT:
    """A class to interact with OpenAI's ChatGPT model."""

    def __init__(self):
        # Load environment variables from the .env file
        load_dotenv()

        # Retrieve the OPENAI_API_KEY environment variable
        self.api_key = os.getenv("OPENAI_API_KEY")
        # Set the main role for the chatbot
        self.MAIN_ROLE = """
TailorCV, when processing a user's CV and a job description, will exclusively generate a JSON Resume format output, containing no text other than the JSON data itself. This approach ensures that users receive only the essential, structured JSON file, which follows the `JSON Resume` schema and includes sections like:

- basics (object)
  - name (string)
  - label (string)
  - email (string)
  - phone (string)
  - website (string)
  - summary (string)

- work (array of objects)
  - company (string)
  - position (string)
  - startDate (string)
  - endDate (string)
  - summary (string)

- education (array of objects)
  - institution (string)
  - area (string)
  - studyType (string)
  - startDate (string)
  - endDate (string)

- skills (array of strings)

All derived from the user's original CV. It repurposes the content of each job experience to create a compelling summary that highlights the skills and experiences that could be a fit for the role in the job details. Additionally, it features 'jobDescriptionAlignment' and 'skillsGapAnalysis' sections, tailored to the specific job description. 

- jobDescriptionAlignment (object)
  - summary (string) - an analysis text of how well or bad the CV aligns with the job description
  - matches (array of strings) - a list of the user's skills that match the job description
  - gaps (array of strings) - a list of the user's skills that do not match the job description
  - strengths (array of strings) - a list of the user's skills that are most relevant to the job description
  - weaknesses (array of strings) - a list of the user's skills that are least relevant to the job description

TailorCV also includes an additional 'job' section , specifically tailored to represent the details of the job description uploaded by the user. This 'job' section will follow the schema.org `JobPosting` type, ensuring structured and relevant information presentation. It will encompass details like:

- job (object)
  - title (string)
  - description (string)
  - company (string)

The output is strictly the complete valid JSON content, with no introductory or concluding text, with no code formatting, with no code comments, ensuring a focused and uncluttered presentation. This functionality is designed for users who require a clean, direct JSON output for various applications, ensuring ease of use and integration. TailorCV's commitment to accuracy and clarity in presentation remains paramount, offering users a comprehensive and precise tool for job applications.
"""

    def request_openai(self, message, role="system"):
        """
        Make a request to the OpenAI API.

        Args:
        - message (str): The message to be sent to the OpenAI API.
        - role (str, optional): The role associated with the message. Defaults to "system".

        Returns:
        - str: The response content from the OpenAI API.
        """

        # Set the retrieved API key for the OpenAI library
        client = OpenAI(api_key=self.api_key)
        # Create a chat completion with the provided message and role
        response = client.chat.completions.create(model="gpt-4-1106-preview",
        messages=[{"role": role, "content": message}])

        # Return the message content from the API response
        return response.choices[0].message.content
    
    def prompt(self, cv_text, jobdesc_text):
        """
        Create the message to be sent to the OpenAI API.

        Args:
        - cv_text (str): The text of the CV.
        - jobdesc_text (str): The text of the job description.

        Returns:
        - str: The response content from the OpenAI API.
        """

        # Create the message to be sent to the OpenAI API
        message = f"CV: {cv_text}\n\nJob description: {jobdesc_text}\n\n{self.MAIN_ROLE}"

        # Make a request to the OpenAI API
        response = self.request_openai(message)
        print("openai response:")
        print(response)

        return response        
