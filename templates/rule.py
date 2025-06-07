"""Rule template generation"""

from templates.base import BaseTemplate


class RuleTemplate(BaseTemplate):
    """Template generator for PCX rules"""

    def generate_commitment_rule(
        self,
        report: str,
        job: str,
        store_number: str,
        variable: str,
        queue: str,
        sequence: int = 23
    ) -> str:
        """Generate a commitment book rule with begin/end components"""

        # Format store number with leading zero if needed
        formatted_store = (
            f"0{store_number}" if len(store_number) == 3 else store_number
        )

        # Build rule description
        folder_dest = f"/Reports/{report}-{job}~{formatted_store}/"
        printer_dest = f"{queue}~STORE{store_number}~001"
        description = f"{folder_dest}  [{printer_dest}]"

        # Generate main rule block
        rule_fields = {
            "RULESETNAME": f"{report}-{job}",
            "SEQUENCE": str(sequence),
            "DESCRIPTION": description,
            "INACTIVE": "N",
            "PAGEEXCLUSIVE": "N",
            "BEGINENDRULE": "Y",
            "ENDEXCLUSIVE": "Y",
            "BYPASSFIRSTPAGEENDCHECK": "Y",
            "RULESETEXCLUSIVE": "N",
            "DONOTDELIVERPAGETODEST": "N",
            "DESTINATIONNAME": folder_dest,
        }

        rule_block = self.generate_block("RULE", rule_fields)

        # Add second destination name manually (can appear multiple times)
        rule_block += f"\n    DESTINATIONNAME           = {printer_dest}"

        # Generate begin component
        begin_component = self.generate_rule_component(
            variable=variable,
            operator="Equal",
            value=formatted_store,
            is_end_component=False
        )

        # Generate end component
        end_component = self.generate_rule_component(
            variable=variable,
            operator="Not Equal",
            value=formatted_store,
            is_end_component=True
        )

        return f"{rule_block}\n{begin_component}\n{end_component}"

    def generate_rule_component(
        self,
        variable: str,
        operator: str,
        value: str,
        is_end_component: bool = False,
        compare_length: int = 4
    ) -> str:
        """Generate a rule component block"""

        component_fields = {
            "OPENPARENTHESISCOUNT": "0",
            "VARIABLE": variable,
            "OPERATOR": operator,
            "VALUE": value,
            "COMPARELENGTH": str(compare_length),
            "CLOSEPARENTHESISCOUNT": "0",
            "ENDCOMPONENT": "Y" if is_end_component else "N",
            "ISROWCOLLEN": "N",
            "ISROWCOLROWCOL": "N",
            "ENFORCEBOUNDARY": "N",
            "NUMERICCOMPARE": "N",
            "BOOLEANCOMPARE": "N",
            "CASESENSITIVE": "N",
            "CONTAINSWILDCARD": "N",
            "CONTAINSVARIABLE": "N",
            "USEPREVIOUSPAGEVALUE": "N"
        }

        component_block = self.generate_block(
            "RULECOMPONENT", component_fields
        )

        # Indent the component block (it's nested under RULE)
        indented_lines = [
            "    " + line
            for line in component_block.split("\n")
        ]

        return "\n".join(indented_lines)

    def generate(self, **kwargs) -> str:
        """Generic generate method - routes to specific generators"""
        if "report" in kwargs and "job" in kwargs:
            return self.generate_commitment_rule(**kwargs)
        else:
            raise ValueError("Missing required parameters for rule generation")
