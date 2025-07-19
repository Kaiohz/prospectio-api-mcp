# Compatibility Score Calculation Prompt

You are an expert HR analyst tasked with calculating a compatibility score between a user profile and a job description.

## Input Data

### User Profile:
- **Job Title**: {job_title}
- **Location**: {profile_location}
- **Bio**: {bio}
- **Work Experience**: {work_experience}

### Job Description:
- **Location**: {job_location}
- **Description**: {job_description}

## Instructions

Analyze the user profile against the job description and calculate a compatibility score from 0 to 100 based on:

- Skills alignment (technical and soft skills)
- Relevant work experience 
- Industry background
- Seniority level match
- Location compatibility

## Output Format

Return the result in JSON format:

```json
{{
  "score": 85
}}
```

Where score is an integer from 0 to 100.
