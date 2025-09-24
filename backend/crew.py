
from crewai import Crew, Process
from agents import (
    product_manager,
    market_research_analyst_pm,
    lead_software_engineer,
    product_designer,
    marketing_manager,
    content_strategist,
    seo_specialist,
    social_media_manager,
    hr_manager,
    employee_relations_specialist,
    legal_compliance_officer,
    talent_acquisition_specialist
)
from tasks import create_product_tasks, create_marketing_tasks, create_hr_tasks

def create_product_crew(idea):
    tasks = create_product_tasks(idea)
    return Crew(
        agents=[product_manager, market_research_analyst_pm, lead_software_engineer, product_designer],
        tasks=tasks,
        process=Process.sequential,
        verbose=True
    )

def create_marketing_crew(idea):
    tasks = create_marketing_tasks(idea)
    return Crew(
        agents=[marketing_manager, content_strategist, seo_specialist, social_media_manager],
        tasks=tasks,
        process=Process.sequential,
        verbose=True
    )

def create_hr_crew(idea):
    tasks = create_hr_tasks(idea)
    return Crew(
        agents=[hr_manager, employee_relations_specialist, legal_compliance_officer, talent_acquisition_specialist],
        tasks=tasks,
        process=Process.sequential,
        verbose=True
    )
