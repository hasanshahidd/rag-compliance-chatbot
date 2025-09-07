# Compliance Gap Analysis Report

## Summary

### Query: What are the access control policies?

**Policy Section**: 4.4

**Response**: [INFERRED] Based on the policy document: to prevent unauthorized access, misuse, or compromise of sensitive data

**Compliance Status**: Non-Compliant

**Audit Priority (Risk Level)**: High

**PCI-DSS Gaps**:

- PCI-DSS 8.1.6: Missing Limit repeated access attempts by locking out the user ID after not more than six attempts.

- PCI-DSS 8.1.7: Missing Set lockout duration to a minimum of 30 minutes or until an administrator enables the account.

- PCI-DSS 12.8.1: Missing Maintain a list of service providers with whom cardholder data is shared.

**ISO 27001 Gaps**:

- ISO 27001 A.9.4.2: Missing Secure authentication procedures to control access to information systems.

- ISO 27001 A.9.4.4: Missing Use of privileged utility programs restricted and monitored.



### Query: How does the policy address encryption?

**Policy Section**: 4.34

**Response**: The provided policy does not explicitly address encryption. However, it mentions the installation of antivirus/anti-malware software on all mobile devices connected to the Bank's network (Section 6). This can be inferred to imply some level of encryption, but it is not a direct reference to encryption.

To achieve PCI-DSS compliance, encryption is required for sensitive data, such as credit card information. However, the provided policy does not explicitly mention encryption for sensitive data.

To achieve ISO 27001 compliance, encryption is recommended for sensitive data, but it is not a requirement. The policy's lack of explicit mention of encryption for sensitive data may not meet the requirements of these compliance standards.

Inferred compliance status: Partially compliant with PCI-DSS and ISO 27001 standards due to the lack of explicit mention of encryption for sensitive data.

**Compliance Status**: Non-Compliant

**Audit Priority (Risk Level)**: High

**PCI-DSS Gaps**:

- PCI-DSS 3.5.4: Missing Store cryptographic keys in the fewest possible locations.

- PCI-DSS 3.6.4: Missing Periodic cryptographic key changes as per defined cryptoperiod.

**ISO 27001 Gaps**:

- ISO 27001 A.10.1.1: Missing Policy on the use of cryptographic controls.



### Query: What are the vulnerability management procedures?

**Policy Section**: 4.16

**Response**: Based on the provided context, the vulnerability management procedures are outlined in point 5 of the document: "Plan, perform, and review vulnerability scanning and Penetration Testing." Additionally, point 6 mentions engaging external consultants for Information Security Assessment and Penetration Testing.

The procedures appear to be in line with PCI-DSS requirements for vulnerability management. The Bank is required to:

* Plan and perform vulnerability scanning and penetration testing
* Review the results and implement necessary remediation
* Engage external consultants for Information Security Assessment and Penetration Testing

The procedures are also likely to be in line with ISO 27001 requirements for vulnerability management, which include:

* Identifying and assessing vulnerabilities
* Implementing remediation measures
* Reviewing and updating vulnerability management procedures

However, it is not explicitly stated in the provided context whether the procedures are compliant with ISO 27001 or not.

**Compliance Status**: Non-Compliant

**Audit Priority (Risk Level)**: High

**PCI-DSS Gaps**:

- PCI-DSS 11.2: Missing Run internal and external vulnerability scans at least quarterly.

**ISO 27001 Gaps**:

- ISO 27001 A.12.6.1: Missing Management of technical vulnerabilities.



### Query: What is the incident response plan?

**Policy Section**: 4.33

**Response**: Based on the provided context, it appears that the incident response plan is part of the overall Information Security Policy, which is aligned with regulatory requirements, including PCI-DSS v3.2 and ISO 27001:2005 guidelines.

However, the specific details of the incident response plan are not explicitly mentioned in the provided context. 

But, it can be inferred that the Bank has a Security Operation Center (SOC) as mentioned in point 7 of the context (Version 4.0) which is responsible for:

- Developing and maintaining the capability to effectively monitor available logs to identify and report Information Security Incidents
- Analyzing reported incidents and giving recommendations to ensure that exposures of incidents are contained and recovery achieved within specified timelines

Additionally, the Bank has a Cyber Security roadmap (point 11 of the context) which is developed in coordination with relevant stakeholders and is monitored for its implementation.

Therefore, it can be inferred that the Bank has a structured approach to incident response, but specific details such as incident response procedures, roles and responsibilities, and incident classification criteria are not explicitly mentioned in the provided context.

**Compliance Status**: Non-Compliant

**Audit Priority (Risk Level)**: High

**PCI-DSS Gaps**:

- PCI-DSS 12.10: Missing Implement an incident response plan.

**ISO 27001 Gaps**:

- ISO 27001 A.16.1: Missing Management of information security incidents.



### Query: How are passwords managed?

**Policy Section**: 4.5

**Response**: The provided Information Security Policy document outlines the management of passwords as follows:

- Passwords are required for access to any system, in addition to a unique user ID.
- Passwords must meet complexity requirements, including being at least eight characters long for normal users.
- Passwords must be communicated to users in a secure manner.
- One-time passwords must be used and changed upon the first login attempt where the application supports this feature.
- Community strings for Simple Network Management Protocol (SNMP) must be defined as something other than the standard defaults.
- Users are not allowed to share their passwords with any other user.
- Passwords must not be stored by users in clear text on the computer system.

This password management policy appears to be compliant with PCI-DSS and ISO 27001 standards, as it addresses password complexity, secure password communication, and password storage. However, a more detailed analysis of the policy's implementation and enforcement is required to confirm full compliance.

**Compliance Status**: Non-Compliant

**Audit Priority (Risk Level)**: High

**PCI-DSS Gaps**:

- PCI-DSS 8.2.3: Missing Passwords must be changed at least every 90 days.

- PCI-DSS 8.2.4: Missing Password complexity requirements (uppercase, lowercase, number, special character).

- PCI-DSS 8.3: Missing Multi-factor authentication for sensitive transactions.

**ISO 27001 Gaps**:

- ISO 27001 A.9.2.4: Missing Management of secret authentication information.



### Query: What are the logging and monitoring policies?

**Policy Section**: 4.12

**Response**: Based on the provided context, the logging and monitoring policies are as follows:

* The system shall maintain a record of all approved mobile devices connecting/accessing the network and information (Section 2).
* Appropriate controls and tracing through logs shall be available for all systems to monitor activities of privileged users (Section 7).
* The Information Security division has the right to inspect logs at any time or ask to show the same with reference to any system/application/device or an individual in question for a specified time period (Section 3).
* ITSC shall review significant Information/Cyber Security incidents upon submission on a regular basis (Section 4).
* ITSC shall review and determine the adequacy of the bank’s training plan including information/cyber security training for the staff (Section 4).

In terms of compliance status, these policies appear to align with the requirements of PCI-DSS and ISO 27001. Specifically:

* PCI-DSS requires the maintenance of a record of all approved devices connecting to the network (Requirement 10.5).
* PCI-DSS requires the implementation of logging and monitoring controls to detect and respond to unauthorized access (Requirement 10.6).
* ISO 27001 requires the implementation of logging and monitoring controls to detect and respond to security incidents (Clause 12.6).

However, it is essential to note that the provided context is a comprehensive information security policy document, and the logging and monitoring policies may be part of a broader set of policies and procedures. Therefore, a more detailed analysis of the document is necessary to determine the full compliance status of the logging and monitoring policies.

**Compliance Status**: Non-Compliant

**Audit Priority (Risk Level)**: Medium

**PCI-DSS Gaps**:

- PCI-DSS 10.2: Missing Implement audit trails to reconstruct events.

**ISO 27001 Gaps**:

- ISO 27001 A.12.4: Missing Logging and monitoring of information processing facilities.



### Query: What is the data retention policy?

**Policy Section**: 4.20

**Response**: The data retention policy is not explicitly stated in the provided context. However, it can be inferred that the bank has a data retention policy in place, as mentioned in the "Data Backup Security" Section 4.9, which states that a backup of network device configurations shall be taken as per this section.

In terms of compliance, the data retention policy is a requirement for PCI-DSS (Payment Card Industry Data Security Standard) and ISO 27001 (International Organization for Standardization 27001). PCI-DSS requires that sensitive authentication data shall not be stored after authorization, while ISO 27001 requires that an organization shall maintain a record of all security-related events.

Based on the provided context, it appears that the bank has a data backup and security policy in place, which includes the retention of certain data for a certain period. However, the specific data retention policy is not clearly stated, and further information is required to determine the bank's compliance status with PCI-DSS and ISO 27001.

**Compliance Status**: Non-Compliant

**Audit Priority (Risk Level)**: Low

**PCI-DSS Gaps**:

- PCI-DSS 3.1: Missing Retain cardholder data only as long as necessary.

**ISO 27001 Gaps**:

- ISO 27001 A.18.1.3: Missing Protection of records.



### Query: How is supplier risk managed?

**Policy Section**: 4.29

**Response**: Supplier risk management is addressed in the context of Information Security Policy, specifically in points 4 and 5 under section 3. The policy requires maintaining a list of B2B partners and ensuring adequate security measures are taken while establishing electronic relations (point 4). Additionally, it is stated that the service provider must be compliant with PCI-DSS requirements where applicable, and the Bank's Information Security policy (point 5).

This indicates that the Bank has established procedures to manage supplier risk, including ensuring that suppliers adhere to the Bank's security standards and regulatory requirements. However, the level of detail provided is limited, and it is unclear how the Bank assesses and mitigates supplier risks.

Compliance status: Partially compliant. The Bank has established procedures for managing supplier risk, but the level of detail and the effectiveness of these procedures are not fully clear.

**Compliance Status**: Non-Compliant

**Audit Priority (Risk Level)**: Medium

**PCI-DSS Gaps**:

- PCI-DSS 12.8: Missing Maintain service provider agreements that address security requirements.

**ISO 27001 Gaps**:

- ISO 27001 A.15.1: Missing Information security in supplier relationships.



### Query: What is the physical security policy?

**Policy Section**: 4.7

**Response**: Unfortunately, the provided context does not explicitly mention a physical security policy. However, it does cover various aspects of information security, including network security, access control, and encryption. 

While there is no direct mention of physical security measures such as access control, video surveillance, or alarm systems, we can infer that the Bank may have some level of physical security in place, given the emphasis on protecting sensitive data and the presence of various security policies and procedures.

However, to confirm the presence and adequacy of a physical security policy, further review of the Bank's security policies or procedures is necessary.

**Compliance Status**: Non-Compliant

**Audit Priority (Risk Level)**: Low

**PCI-DSS Gaps**:

- PCI-DSS 9.1: Missing Secure areas to protect cardholder data.

**ISO 27001 Gaps**:

- ISO 27001 A.11: Missing Physical and environmental security.



### Query: How does the organization ensure business continuity?

**Policy Section**: 4.25

**Response**: Based on the provided Information Security Policy document, the organization ensures business continuity through the following measures:

1. **IT Service Continuity (ITSC)**: The Bank shall formulate an ITSC with senior officials to review and determine the adequacy of the bank's training plan, including information/cyber security training for the staff (Section 1.5.2).
2. **Cyber Security Action Plan**: The ITSC shall periodically inform the Board of Directors on the latest developments on cyber security action plan, its implementation status, a summary report on major threats, attacks faced by the Bank, and their estimated impact on its operations (Section 1.4.2(d)).
3. **Incident Response**: The ITSC shall review significant Information/Cyber Security incidents upon submission on a regular basis (Section 1.4.2(c)).
4. **Business Continuity Planning**: Although not explicitly mentioned, the organization's emphasis on IT service continuity and incident response suggests that business continuity planning is a priority.

Compliance Status: The organization appears to have a solid foundation for ensuring business continuity, with a focus on IT service continuity, incident response, and training. However, a more detailed business continuity plan and procedures would be beneficial to ensure compliance with relevant standards, such as ISO 22301.

Recommendation: The organization should consider developing a comprehensive business continuity plan that outlines procedures for responding to disruptions, maintaining IT services, and ensuring the confidentiality, integrity, and availability of critical business systems and data.

**Compliance Status**: Non-Compliant

**Audit Priority (Risk Level)**: Medium

**PCI-DSS Gaps**:

- PCI-DSS 12.10.3: Missing Test incident response and business continuity plans regularly.

**ISO 27001 Gaps**:

- ISO 27001 A.17: Missing Information security aspects of business continuity management.


