
from crewai import Task
from agents import (
    hr_manager,
    employee_relations_specialist,
    legal_compliance_officer,
    talent_acquisition_specialist
)

def create_product_tasks(idea):
    return [
        Task(
            description=f'Analyze the market for the product idea: {idea}.',
            expected_output='A detailed market analysis report.',
            agent_name='Market Research Analyst'
        ),
        Task(
            description=f'Assess the technical feasibility of the product idea: {idea}.',
            expected_output='A technical feasibility report.',
            agent_name='Lead Software Engineer'
        ),
        Task(
            description=f'Define the user experience (UX) and user interface (UI) for the product idea: {idea}.',
            expected_output='A UX/UI design document.',
            agent_name='Product Designer'
        ),
        Task(
            description=f'Create a comprehensive Product Requirements Document (PRD) for the product idea: {idea}.',
            expected_output='A final, well-structured PRD.',
            agent_name='Product Manager'
        )
    ]

def create_marketing_tasks(idea):
    return [
        Task(
            description=f'Develop a content strategy for the marketing idea: {idea}.',
            expected_output='A detailed content strategy document.',
            agent_name='Content Strategist'
        ),
        Task(
            description=f'Create an SEO strategy for the marketing idea: {idea}.',
            expected_output='A comprehensive SEO strategy.',
            agent_name='SEO Specialist'
        ),
        Task(
            description=f'Develop a social media plan for the marketing idea: {idea}.',
            expected_output='A detailed social media plan.',
            agent_name='Social Media Manager'
        ),
        Task(
            description=f'Create a comprehensive marketing campaign plan for the idea: {idea}.',
            expected_output='A final, well-structured marketing campaign plan.',
            agent_name='Marketing Manager'
        )
    ]

def create_hr_tasks(idea):
    return [
        Task(
            description=f'Analyze the impact of the HR idea on employees: {idea}.',
            expected_output='A detailed employee impact analysis.',
            agent=employee_relations_specialist
        ),
        Task(
            description=f'Review the HR idea for legal compliance: {idea}.',
            expected_output='A legal compliance report.',
            agent=legal_compliance_officer
        ),
        Task(
            description=f'Assess the impact of the HR idea on talent acquisition and retention: {idea}.',
            expected_output='A talent acquisition and retention impact report.',
            agent=talent_acquisition_specialist
        ),
        Task(
            description=f'Create a comprehensive HR policy or program proposal for the idea: {idea}.',
            expected_output='A final, well-structured HR policy or program proposal.',
            agent=hr_manager
        )
    ]
