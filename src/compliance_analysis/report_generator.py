import json
import logging
from pathlib import Path
from src.rag_pipeline.query_engine import query_knowledge_base

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Risk mapping for audit priority
RISK_LEVELS = {
    "access control": "High",
    "encryption": "High",
    "incident response": "High",
    "vulnerability": "High",
    "logging": "Medium",
    "monitoring": "Medium",
    "supplier": "Medium",
    "data retention": "Low",
    "physical security": "Low",
    "business continuity": "Medium",
    "password": "High"
}

def assign_risk_level(query: str) -> str:
    """Assign audit priority (risk level) based on query keywords."""
    query_lower = query.lower()
    for keyword, risk in RISK_LEVELS.items():
        if keyword in query_lower:
            return risk
    return "Low"

def load_compliance_mapping(mapping_path="data/mappings/compliance_mapping.json"):
    """Load compliance mapping from JSON."""
    try:
        with open(mapping_path, 'r', encoding='utf-8') as f:
            return json.load(f).get("mappings", [])
    except Exception as e:
        logger.error(f"Error loading compliance mapping: {e}")
        return []

def analyze_compliance(response: str, section: str, mappings: list):
    """Analyze response for compliance status and gaps using mapping JSON."""
    if not mappings:
        return "Unknown", ["Compliance mapping not found"], [], []

    for mapping in mappings:
        if mapping.get("policy_section", "").startswith(section):
            pci_dss = mapping.get("pci_dss", [])
            iso_27001 = mapping.get("iso_27001", [])
            pci_gaps, iso_gaps, gaps = [], [], []

            # Check PCI-DSS clauses
            for clause in pci_dss:
                desc = clause.get("description", "").lower()
                if desc and desc not in response.lower():
                    gap_text = f"PCI-DSS {clause['clause']}: Missing {clause['description']}"
                    gaps.append(gap_text)
                    pci_gaps.append(gap_text)

            # Check ISO 27001 clauses
            for clause in iso_27001:
                desc = clause.get("description", "").lower()
                if desc and desc not in response.lower():
                    gap_text = f"ISO 27001 {clause['clause']}: Missing {clause['description']}"
                    gaps.append(gap_text)
                    iso_gaps.append(gap_text)

            # Determine compliance status
            if not gaps:
                status = "Compliant"
            elif len(gaps) < (len(pci_dss) + len(iso_27001)):
                status = "Partially Compliant"
            else:
                status = "Non-Compliant"

            return status, gaps, pci_gaps, iso_gaps

    return "Unknown", ["Section not found in compliance mapping"], [], []

def generate_report(output_path="data/output/compliance_report.md"):
    """Generate compliance gap analysis report."""
    queries = [
        {"query": "What are the access control policies?", "section": "4.4"},
        {"query": "How does the policy address encryption?", "section": "4.34"},
        {"query": "What are the vulnerability management procedures?", "section": "4.16"},
        {"query": "What is the incident response plan?", "section": "4.33"},
        {"query": "How are passwords managed?", "section": "4.5"},
        {"query": "What are the logging and monitoring policies?", "section": "4.12"},
        {"query": "What is the data retention policy?", "section": "4.20"},
        {"query": "How is supplier risk managed?", "section": "4.29"},
        {"query": "What is the physical security policy?", "section": "4.7"},
        {"query": "How does the organization ensure business continuity?", "section": "4.25"}
    ]

    mappings = load_compliance_mapping()
    report_content = ["# Compliance Gap Analysis Report\n", "## Summary\n"]

    for q in queries:
        logger.info(f"Processing query: {q['query']}")
        response = query_knowledge_base(q["query"])
        status, gaps, pci_gaps, iso_gaps = analyze_compliance(response, q["section"], mappings)
        risk = assign_risk_level(q["query"])

        report_content.append(f"### Query: {q['query']}\n")
        report_content.append(f"**Policy Section**: {q['section']}\n")
        report_content.append(f"**Response**: {response}\n")
        report_content.append(f"**Compliance Status**: {status}\n")
        report_content.append(f"**Audit Priority (Risk Level)**: {risk}\n")

        # Framework-specific findings
        report_content.append("**PCI-DSS Gaps**:\n")
        if pci_gaps:
            for gap in pci_gaps:
                report_content.append(f"- {gap}\n")
        else:
            report_content.append("- None\n")

        report_content.append("**ISO 27001 Gaps**:\n")
        if iso_gaps:
            for gap in iso_gaps:
                report_content.append(f"- {gap}\n")
        else:
            report_content.append("- None\n")

        report_content.append("\n")

    # Save report
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(report_content))
    logger.info(f"Report generated at {output_path}")

if __name__ == "__main__":
    generate_report()
