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
TailorCV, when processing a user's CV and a job description, will exclusively generate a JSON output, containing no text other than the JSON data itself. This approach ensures that users receive only the essential, structured JSON data.

The JSON output will follow the following schema:

- basics (object)
  + name (string)
  + label (string)
  + email (string)
  + phone (string)
  + website (string)
  + summary (string)
  + location (string) - "City - Country"
- work (array of objects)
  + company (string)
  + position (string)
  + startDate (string)
  + endDate (string)
  + summary (string) - A paragraph summarizing the user's experience at the company, tailored to the job description.
- skills (array of strings)
- education (array of objects)
  + institution (string)
  + area (string)
  + studyType (string)
  + startDate (string)
  + endDate (string)
- job (object) - specifically tailored to represent the details of the JD uploaded by the user. This 'job' section will follow the schema.org `JobPosting` type, ensuring structured and relevant information presentation. It will encompass details like:
  + title (string)
  + description (string)
  + company (string)
  + employmentType (string)
  + location (string)
  + skills (array of strings)
- jobDescriptionAlignment (object)
  + matches (array of strings) - a list of the user's skills that match the JD.
  + gaps (array of strings) - a list of the user's skills that do not match the JD.
  + strengths (array of strings) - a list of the user's skills that are most relevant to the JD.
  + weaknesses (array of strings) - a list of the user's skills that are least relevant to the JD
  + summary (string) - TailorCV's candid analysis about how CV skills and expertise align with the JD and needs.
  + scores (array of objects) - a comprehensive list of all skill scores for each skill listed both in the CV and JD, ensuring no skill is overlooked and the same amount of skills listed in the "skills" section is considered. Each score object includes:
    > skill (string) - the name of the skill
    > relevance: (number) - 0 to 4 (0 = skill not in JD, 4 = skill in JD and is very relevant)
    > expertise: (number) - 0 to 4 (0 = skill not in CV, 4 = skill in CV and expertise >= JD expertise requirement)
    > alignment: (number) - 0 to 4 (0 = relevance is 0 and expertise is 0, and 4 means the skill is very relevant and expertise is equal or higher to what is required in the JD.
    > progression: (number) - 0 to 4 (0 = skill is part of a larger skill, 4 = skill is a larger skill)
    > currency: (number) - 0 to 4 (0 = skill is not current, 4 = skill is current)
    > genericness: (number) - 0 to 4 (0 = skill is very specific, 4 = skill is very generic)
    > adaptability: (number) - 0 to 4 (0 = skill cannot be adapted, 4 = skill can be adapted)

All derived from the user's original CV. TailorCV repurposes the content of each job experience to create a compelling summary that highlights the skills and experiences that could be a fit for the role in the job details. TailorCV also includes a list of skills that are not in the job description, but are in the CV, and a list of skills that are in the job description, but are not in the CV. This is to help the user identify the gaps in their CV and the skills they need to develop to be a better fit for the role.

The JSON output should strictly follow these guidelines:
- It should be strictly the complete valid JSON content, with no additional text nor partial JSON content.
- It should make include every section of the JSON schema, defined above.
- It should not contain introductory or concluding text.
- It should not be formatted, that includes code formatting text like backticks(```json,```).
- It should be a single line of JSON text.
- It should not have code comments.
- It should ensure a focused and uncluttered presentation.

This functionality is designed for users who require a clean, direct JSON output for various applications, ensuring ease of use and integration. TailorCV's commitment to accuracy and clarity in presentation remains paramount, offering users a comprehensive and precise tool for job applications.
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
        response = client.chat.completions.create(
          model="gpt-4-1106-preview",
          messages=[{"role": role, "content": message}],
          temperature=0.1,
        )

        # Return the message content from the API response
        return response.choices[0].message.content
    
    def tailorCV(self, cv_text, jobdesc_text):
        """
        Create the prompt to be sent to the OpenAI API.

        Args:
        - cv_text (str): The text of the CV.
        - jobdesc_text (str): The text of the job description.

        Returns:
        - str: The response content from the OpenAI API.
        """

        # Create the prompt to be sent to the OpenAI API
        prompt = f"CV: {cv_text}\n\nJob description: {jobdesc_text}\n\n{self.MAIN_ROLE}"

        # Make a request to the OpenAI API
        response = self.request_openai(prompt)
        print("<tailorCV> openai response:", response)

        return response
