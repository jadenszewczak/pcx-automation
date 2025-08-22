"""Destination template generation"""

from typing import Any
from templates.base import BaseTemplate


class DestinationTemplate(BaseTemplate):
    def generate_printer(
        self,
        queue: str,
        store_number: str,
        store_name: str,
        address: str,
        city_state_zip: str,
        copy_num: str = "001"
    ) -> str:
        """Generate printer destination block"""

        template = f"""ADD DESTINATION
    NAME                      = {queue}~STORE{store_number}~{copy_num}
    TYPE                      = Print Server
    PRINTSERVER               = vpsx
    PRINTERNAME               = {self.get_printer_name(queue)}
    FILENAME                  = &FILEPRE
    COPIES                    = 2
    TITLE                     = &ADVREPORTDESC
    CLASS                     = &RPT_{queue}_CLASS
    FORM                      = &RPT_{queue}_FORM
    JOBNAME                   = &RPT_WRITER
    USERDATA4                 = OU=&RPT_{queue}_OUTPUT PA=&RPT_DFLTJ_PAGEFMT
    USERDATA5                 = CO=&RPT_{queue}_CPYGRP CH=&RPT_DFLTJ_CHARS
    USERDATA6                 = {store_number}(GP)STORE{store_number}
    USERDATA10                = FLASH=&RPT_{queue}_FLASH
    USERDATA11                = {store_name}
    USERDATA12                = {address}
    USERDATA14                = {city_state_zip}
    USERDATA15                = _"""

        return template.strip()

    def generate_folder(self, report: str, job: str, identifier: str) -> str:
        """Generate folder destination block"""

        # Format identifier with leading zero if needed
        formatted_id = f"0{identifier}" if len(identifier) == 3 else identifier

        template = f"""ADD DESTINATION
    NAME                       = /Reports/{report}-{job}~{formatted_id}/
    TYPE                       = Folder
    IMPORTFOLDERPATH           = /Reports/{report}-{job}~{formatted_id}/
    DOCUMENTNAME               = &ADVREPORT.&FILETYPE
    TITLE                      = &ADVREPORTDESC"""

        return template.strip()

    def get_printer_name(self, queue: str) -> str:
        """Get printer name from queue mapping"""
        from config.mappings import VPSX_QUEUES
        return VPSX_QUEUES.get(queue, queue)

    def generate(self, **kwargs: Any) -> str:
        """Generic generate method - routes to specific generators"""
        if 'queue' in kwargs:
            # Extract and cast parameters for printer generation
            queue = str(kwargs.get('queue', ''))
            store_number = str(kwargs.get('store_number', ''))
            store_name = str(kwargs.get('store_name', ''))
            address = str(kwargs.get('address', ''))
            city_state_zip = str(kwargs.get('city_state_zip', ''))
            copy_num = str(kwargs.get('copy_num', '001'))

            return self.generate_printer(
                queue=queue,
                store_number=store_number,
                store_name=store_name,
                address=address,
                city_state_zip=city_state_zip,
                copy_num=copy_num
            )
        elif 'report' in kwargs and 'job' in kwargs:
            # Extract and cast parameters for folder generation
            report = str(kwargs.get('report', ''))
            job = str(kwargs.get('job', ''))
            identifier = str(kwargs.get('identifier', ''))

            return self.generate_folder(
                report=report,
                job=job,
                identifier=identifier
            )
        else:
            raise ValueError(
                "Missing required parameters for destination generation"
            )
