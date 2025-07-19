from domain.entities.job import Job, JobEntity
from domain.entities.leads import Leads
from domain.entities.leads_result import LeadsResult
from domain.entities.profile import Profile
from domain.ports.compatibility_score import CompatibilityScorePort
import asyncio

class LeadsProcessor:
    def __init__(self, compatibility_score_port: CompatibilityScorePort, concurrent_calls):
        self.compatibility_score_port = compatibility_score_port
        self.semaphore = asyncio.Semaphore(concurrent_calls)

    async def calculate_statistics(self, leads: Leads) -> LeadsResult:
        nb_of_companies = len(leads.companies.root) if leads.companies else 0
        nb_of_jobs = len(leads.jobs.root) if leads.jobs else 0
        nb_of_contacts = len(leads.contacts.root) if leads.contacts else 0
        
        return LeadsResult(
            companies=f"Insert of {nb_of_companies} companies",
            jobs=f"insert of {nb_of_jobs} jobs",
            contacts=f"insert of {nb_of_contacts} contacts",
        )
    
    async def calculate_compatibility_scores(self, profile: Profile, jobs: JobEntity) -> JobEntity:
            
        async def calculate_single_score(job: Job):
            async with self.semaphore:
                if not job.description:
                    return job, 0
                result = await self.compatibility_score_port.get_compatibility_score(
                    profile=profile,
                    job_description=job.description,
                    job_location=job.location or ''
                )
                return job, result.score
        
        tasks = [calculate_single_score(job) for job in jobs.root]
        
        results = await asyncio.gather(*tasks)
        
        for job, score in results:
            job.compatibility_score = score

        return jobs
            