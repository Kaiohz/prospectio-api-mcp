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

Analyze the user profile against the job description and calculate a compatibility score from 0 to 100 based on the following weighted criteria:

### Scoring Breakdown (Total: 100 points)

#### 1. Skills Alignment (40 points)
- **Technical Skills (25 points)**: Match between required technical skills and user's expertise
  - Perfect match (all required skills present): 25 points
  - High match (80%+ skills present): 20-24 points
  - Moderate match (60-79% skills present): 15-19 points
  - Low match (40-59% skills present): 10-14 points
  - Poor match (<40% skills present): 0-9 points

- **Soft Skills (15 points)**: Leadership, communication, teamwork abilities
  - Strong evidence of required soft skills: 12-15 points
  - Some evidence: 8-11 points
  - Limited evidence: 4-7 points
  - No evidence: 0-3 points

#### 2. Work Experience Relevance (30 points)
- **Industry Experience (15 points)**:
  - Same industry: 15 points
  - Related industry: 10-14 points
  - Different but transferable: 5-9 points
  - Unrelated industry: 0-4 points

- **Role Similarity (15 points)**:
  - Identical or very similar role: 15 points
  - Related role with overlap: 10-14 points
  - Some relevant experience: 5-9 points
  - **Special case: Internship mismatch**: If the job is an internship and the candidate is not seeking an internship (or vice versa), assign a very low score (0 points) to reflect a strong mismatch in expectations and suitability.

#### 3. Seniority Level Match (20 points)
- **Experience Level Alignment**:
  - Perfect match (same level): 20 points
  - One level difference: 15-19 points
  - Two levels difference: 10-14 points
  - Overqualified (2+ levels above): 5-9 points
  - Underqualified (2+ levels below): 0-4 points

#### 4. Location Compatibility (10 points)
- **Geographic Match**:
  - Same city/area: 10 points
  - Same region/state: 7-9 points
  - Same country, different region: 4-6 points
  - Different country: 0-3 points
  - Remote work mentioned: Add 5 bonus points if applicable

### Scoring Guidelines
- Be objective and evidence-based in your assessment
- Consider transferable skills and adaptability
- Factor in career progression and growth potential
- Account for remote work flexibility when mentioned

## Output Format

Return the result in JSON format:

```json
{{
  "score": 85
}}
```

Where score is an integer from 0 to 100.
