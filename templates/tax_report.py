"""Tax Report Template Generation"""

from typing import List, Any
from templates.base import BaseTemplate


class TaxReportTemplate(BaseTemplate):
    """Generate tax report configurations"""
    
    TAX_REPORT_JOBS = {
        'TAX001': ['PPA0771R', 'PPA0950W', 'PPA1545R', 'PPA1545X', 'PPA8920R', 'PPA9999R'],
        'TAX001AD': ['PPA1545R', 'PPA1545X'],
        'TAX001FF': ['PPA1545R', 'PPA1545X'],
        'TAX004': ['PPA0951W'],
        'TAX010': ['PPA0951W'],
        'TAX010FD': ['PPA0951W', 'PPA8905R'],
        'TAX010FT': ['PPA0951W', 'PPA8955R'],
        'TAX010HA': ['PPA0951W', 'PPA8906R'],
        'TAX010ST': ['PPA0951W', 'PPA8910R']
    }
    
    def generate_consolidated(self, companies: List[str], reports: List[str]) -> str:
        """Generate consolidated configuration for multiple companies"""
        content = []
        
        for company in companies:
            for report in reports:
                if report not in self.TAX_REPORT_JOBS:
                    continue
                    
                for job in self.TAX_REPORT_JOBS[report]:
                    content.append(self.generate_rule_for_company(report, job, company))
                    content.append("")
        
        return '\n'.join(content)
    
    def generate_rule_for_company(self, report: str, job: str, company: str) -> str:
        """Generate rule for a single company"""
        lines = []
        lines.append("ADD RULE")
        lines.append(f"    RULESETNAME               = {report}-{job}")
        lines.append(f"    SEQUENCE                  = {company}")
        lines.append(f"    DESCRIPTION               = Company {company} - {report}")
        lines.append(f"    INACTIVE                  = N")
        lines.append(f"    PAGEEXCLUSIVE             = N")
        lines.append(f"    BEGINENDRULE              = Y")
        lines.append(f"    ENDEXCLUSIVE              = Y")
        lines.append(f"    BYPASSFIRSTPAGEENDCHECK   = Y")
        lines.append(f"    RULESETEXCLUSIVE          = N")
        lines.append(f"    DESTINATIONNAME           = /Reports/{report}-{job}~{company}/")
        
        # Begin component
        lines.append("    ADD RULECOMPONENT")
        lines.append("        VARIABLE              = &RPT_COMPANY")
        lines.append("        OPERATOR              = Equal")
        lines.append(f"        VALUE                 = {company}")
        lines.append("        COMPARELENGTH         = 3")
        lines.append("        ENDCOMPONENT          = N")
        
        # End component
        lines.append("    ADD RULECOMPONENT")
        lines.append("        VARIABLE              = &RPT_COMPANY")
        lines.append("        OPERATOR              = Not Equal")
        lines.append(f"        VALUE                 = {company}")
        lines.append("        COMPARELENGTH         = 3")
        lines.append("        ENDCOMPONENT          = Y")
        
        return '\n'.join(lines)
    
    def generate(self, **kwargs: Any) -> str:
        """Generic generate method"""
        companies = kwargs.get('companies', [])
        reports = kwargs.get('reports', [])
        return self.generate_consolidated(companies, reports)
