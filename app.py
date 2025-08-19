import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import uuid
import hashlib
import json

# Page configuration
st.set_page_config(
    page_title="Alkhorayef Group - 2025 Shared Services Budgeting System",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== ENHANCED CONFIGURATION DATA ====================

# Admin Credentials (All 5 Departments + Super Admin)
ADMIN_CREDENTIALS = {
    "it_admin": {"password": "itadmin2025", "department": "IT", "name": "IT Department Head"},
    "hr_admin": {"password": "hradmin2025", "department": "HR", "name": "HR Department Head"},
    "legal_admin": {"password": "legaladmin2025", "department": "Legal", "name": "Legal Department Head"},
    "procurement_admin": {"password": "procadmin2025", "department": "Procurement", "name": "Procurement Department Head"},
    "facility_admin": {"password": "faciladmin2025", "department": "Facility_Safety", "name": "Facility & Safety Department Head"},
    "super_admin": {"password": "superadmin2025", "department": "ALL", "name": "Super Administrator"}
}

# Company and Department Lists
ALKHORAYEF_COMPANIES = ["APC", "AIC", "AGC", "APS", "PS", "AWPT", "AMIC", "ACC", "SPC", "Tom Egypt"]
COMPANY_DEPARTMENTS = ["Finance", "Human Resources", "Operations", "Sales", "Marketing", "IT", "Customer Service", "Supply Chain", "Manufacturing", "Executive", "Procurement", "Legal", "Quality Assurance", "Safety & Security"]

# All 5 Shared Service Departments Configuration
SHARED_SERVICE_DEPARTMENTS = {
    "IT": {
        "icon": "💻",
        "title": "Information Technology",
        "description": "Digital transformation, technology infrastructure, enterprise applications, software licensing",
        "color": "#3b82f6"
    },
    "HR": {
        "icon": "👥",
        "title": "Human Resources",
        "description": "Talent management, employee development, HR operations, organizational effectiveness",
        "color": "#10b981"
    },
    "Legal": {
        "icon": "⚖️",
        "title": "Legal Services", 
        "description": "Legal counsel, contract management, compliance, risk management, intellectual property",
        "color": "#8b5cf6"
    },
    "Procurement": {
        "icon": "🛒",
        "title": "Procurement & Supply Chain",
        "description": "Purchasing, vendor management, contracts, supply chain optimization",
        "color": "#f59e0b"
    },
    "Facility_Safety": {
        "icon": "🏢",
        "title": "Facilities & Safety",
        "description": "Facility management, workplace safety, security, environmental compliance",
        "color": "#ef4444"
    }
}

# Enhanced Default Service Data for All 5 Departments
DEFAULT_SERVICES = {
    "IT": {
        "Microsoft 365 E3": {"price_per_user": 82, "setup_cost": 5000, "description": "Premium productivity suite with advanced security and compliance", "contract_duration": 36, "min_commitment": 50},
        "Oracle ERP Cloud": {"price_per_user": 180, "setup_cost": 25000, "description": "Complete enterprise resource planning solution", "contract_duration": 60, "min_commitment": 25},
        "Power BI Premium": {"price_per_user": 75, "setup_cost": 4000, "description": "Advanced business intelligence platform", "contract_duration": 12, "min_commitment": 10},
        "Microsoft Teams Phone": {"price_per_user": 28, "setup_cost": 3000, "description": "Cloud-based phone system integrated with Teams", "contract_duration": 24, "min_commitment": 20},
        "Microsoft Dynamics 365": {"price_per_user": 210, "setup_cost": 30000, "description": "Customer relationship management and enterprise applications suite", "contract_duration": 36, "min_commitment": 15}
    },
    "HR": {
        "Talent Acquisition Platform": {"price_per_user": 120, "setup_cost": 15000, "description": "End-to-end recruitment and hiring platform"},
        "Learning Management System": {"price_per_user": 45, "setup_cost": 8000, "description": "Employee training and development platform"},
        "Performance Management": {"price_per_user": 65, "setup_cost": 12000, "description": "Goal setting and performance review system"},
        "HR Analytics Dashboard": {"price_per_user": 85, "setup_cost": 10000, "description": "Workforce analytics and reporting platform"},
        "Employee Engagement Suite": {"price_per_user": 35, "setup_cost": 5000, "description": "Employee surveys and engagement tracking"}
    },
    "Legal": {
        "Contract Management System": {"price_per_contract": 250, "setup_cost": 20000, "description": "Lifecycle contract management and compliance"},
        "Legal Research Platform": {"price_per_user": 150, "setup_cost": 5000, "description": "Comprehensive legal research and documentation"},
        "Compliance Management": {"price_per_regulation": 500, "setup_cost": 15000, "description": "Regulatory compliance tracking and reporting"},
        "IP Management System": {"price_per_asset": 100, "setup_cost": 12000, "description": "Intellectual property portfolio management"},
        "Legal Document Automation": {"price_per_template": 300, "setup_cost": 8000, "description": "Automated legal document generation"}
    },
    "Procurement": {
        "E-Procurement Platform": {"price_per_transaction": 25, "setup_cost": 18000, "description": "Digital procurement and supplier management"},
        "Supplier Portal": {"price_per_supplier": 120, "setup_cost": 8000, "description": "Supplier onboarding and management portal"},
        "Contract Management": {"price_per_contract": 150, "setup_cost": 12000, "description": "Procurement contract lifecycle management"},
        "Spend Analytics": {"price_per_user": 95, "setup_cost": 10000, "description": "Procurement spend analysis and reporting"},
        "RFQ Management System": {"price_per_event": 500, "setup_cost": 15000, "description": "Request for quotation and bidding platform"}
    },
    "Facility_Safety": {
        "Facility Management System": {"price_per_sq_meter": 12, "setup_cost": 25000, "description": "Comprehensive facility operations management"},
        "Safety Management Platform": {"price_per_employee": 45, "setup_cost": 18000, "description": "Workplace safety tracking and compliance"},
        "Security Access Control": {"price_per_access_point": 180, "setup_cost": 35000, "description": "Physical security and access management"},
        "Environmental Monitoring": {"price_per_monitoring_point": 250, "setup_cost": 15000, "description": "Environmental compliance and monitoring"},
        "Emergency Management": {"price_per_location": 2500, "setup_cost": 20000, "description": "Emergency response and business continuity"},
        "Asset Management": {"price_per_asset": 35, "setup_cost": 12000, "description": "Asset tracking and maintenance scheduling"},
        "Fleet Management": {"price_per_vehicle": 850, "setup_cost": 22000, "description": "Vehicle fleet tracking and maintenance"}
    }
}

# Current License Inventory (IT Department)
DEFAULT_LICENSE_INVENTORY = {
    "Microsoft 365 E3": {"current_count": 150, "contract_end": "2025-12-31", "min_commitment": 50, "can_reduce": False},
    "Oracle ERP Cloud": {"current_count": 75, "contract_end": "2026-06-30", "min_commitment": 25, "can_reduce": False},
    "Power BI Premium": {"current_count": 25, "contract_end": "2025-03-31", "min_commitment": 10, "can_reduce": True}
}

# Enhanced Support Packages
DEFAULT_SUPPORT_PACKAGES = {
    "Basic": {"price": 52000, "support_requests": 50, "training": 0, "reports": 0, "improvement_hours": 0, "description": "Essential support for small teams", "departments": ["IT", "HR", "Legal", "Procurement", "Facility_Safety"]},
    "Bronze": {"price": 195975, "support_requests": 100, "training": 2, "reports": 2, "improvement_hours": 50, "description": "Enhanced support for growing organizations", "departments": ["IT", "HR", "Legal", "Procurement", "Facility_Safety"]},
    "Silver": {"price": 649498, "support_requests": 400, "training": 5, "reports": 5, "improvement_hours": 120, "description": "Comprehensive support for medium enterprises", "departments": ["IT", "HR", "Legal", "Procurement", "Facility_Safety"]},
    "Gold": {"price": 1578139, "support_requests": 1000, "training": 10, "reports": 10, "improvement_hours": 240, "description": "Premium support for large organizations", "departments": ["IT", "HR", "Legal", "Procurement", "Facility_Safety"]},
    "Platinum": {"price": 2500000, "support_requests": 1575, "training": 20, "reports": 15, "improvement_hours": 380, "description": "Enterprise-grade support with dedicated resources", "departments": ["IT", "HR", "Legal", "Procurement", "Facility_Safety"]}
}

# RPA Packages (IT specific)
DEFAULT_RPA_PACKAGES = {
    "Bronze (1 Credit)": {"year_1_total": 88770, "year_2_cost": 10098, "year_3_cost": 10906, "processes_covered": "Up to 2 processes", "implementation_processes": "1 process"},
    "Silver (3 Credits)": {"year_1_total": 285660, "year_2_cost": 30294, "year_3_cost": 32718, "processes_covered": "Up to 5 processes", "implementation_processes": "3 processes"},
    "Gold (5 Credits)": {"year_1_total": 455015, "year_2_cost": 50490, "year_3_cost": 54529, "processes_covered": "Up to 10 processes", "implementation_processes": "5 processes"},
    "Platinum (10 Credits)": {"year_1_total": 869861, "year_2_cost": 100980, "year_3_cost": 109058, "processes_covered": "Up to 20 processes", "implementation_processes": "10 processes"}
}

# Implementation Project Categories by Department
DEFAULT_PROJECT_CATEGORIES = {
    "IT": {
        "🤖 Digital Transformation & Automation": ["RPA Implementation", "Process Automation", "Digital Workflow Management", "Document Management System"],
        "🧠 AI & Advanced Analytics": ["AI Platform Implementation", "Predictive Analytics", "Computer Vision Solutions", "Chatbot Development"],
        "📊 Data & Business Intelligence": ["Data Warehouse Implementation", "Real-time Dashboard Development", "Data Lake Architecture", "Self-Service Analytics"],
        "💼 Enterprise Applications": ["ERP System Implementation", "CRM Deployment", "HCM Implementation", "Supply Chain Management"],
        "☁️ Infrastructure & Cloud": ["Cloud Migration", "Infrastructure Upgrade", "Network Enhancement", "Backup & Disaster Recovery"],
        "🔒 Security & Compliance": ["Cybersecurity Enhancement", "Identity & Access Management", "SIEM Implementation", "Compliance Management"]
    },
    "HR": {
        "👤 Talent Acquisition & Recruitment": ["Recruitment Platform", "Candidate Management", "Interview Management", "Onboarding Automation"],
        "📚 Learning & Development": ["LMS Implementation", "Skills Management", "Training Program Development", "E-Learning Platform"],
        "📈 Performance Management": ["Performance Review System", "Goal Management", "360 Feedback Platform", "Succession Planning"],
        "💰 Compensation & Benefits": ["Compensation Analysis", "Benefits Administration", "Payroll Integration", "Incentive Management"],
        "🔧 HR Technology & Systems": ["HRIS Implementation", "HR Analytics Platform", "Employee Self-Service", "Mobile HR App"],
        "🤝 Employee Relations & Engagement": ["Employee Survey Platform", "Engagement Analytics", "Communication Tools", "Culture Management"]
    },
    "Legal": {
        "🏢 Corporate Legal Services": ["Corporate Governance Platform", "Board Management System", "Regulatory Filing Automation", "Entity Management"],
        "📄 Contract Management & Review": ["Contract Lifecycle Management", "Contract Analytics", "Template Automation", "Approval Workflows"],
        "✅ Compliance & Regulatory Affairs": ["Compliance Management System", "Regulatory Tracking", "Audit Management", "Policy Management"],
        "💡 Intellectual Property Management": ["IP Portfolio Management", "Patent Tracking", "Trademark Management", "IP Analytics"],
        "⚖️ Litigation & Dispute Resolution": ["Case Management System", "Document Discovery", "Legal Hold Management", "Settlement Tracking"],
        "🔍 Legal Technology & Research": ["Legal Research Platform", "Document Automation", "Legal Analytics", "AI-Powered Review"]
    },
    "Procurement": {
        "🛒 Purchase Order Management": ["P2P Platform Implementation", "PO Automation", "Approval Workflow", "Purchase Analytics"],
        "🤝 Supplier & Vendor Management": ["Supplier Portal", "Vendor Onboarding", "Performance Management", "Risk Assessment"],
        "📊 Sourcing & RFQ Management": ["E-Sourcing Platform", "RFQ Automation", "Bid Management", "Supplier Selection"],
        "📄 Contract Management": ["Contract Repository", "Contract Analytics", "Renewal Management", "Compliance Tracking"],
        "💰 Spend Analytics & Reporting": ["Spend Analysis Platform", "Cost Optimization", "Budget Management", "Savings Tracking"],
        "🔧 Procurement Technology": ["Procurement System Integration", "Mobile Procurement App", "AI-Powered Procurement", "Blockchain Implementation"]
    },
    "Facility_Safety": {
        "🏢 Facility Management & Operations": ["CMMS Implementation", "Space Management", "Energy Management", "Maintenance Optimization"],
        "🔒 Security & Access Control": ["Access Control System", "CCTV Management", "Visitor Management", "Security Analytics"],
        "⚠️ Safety & Compliance": ["Safety Management System", "Incident Management", "Training Platform", "Compliance Tracking"],
        "🚨 Emergency Management": ["Emergency Response System", "Crisis Management", "Communication Platform", "Business Continuity"],
        "🌡️ Environmental & Health": ["Environmental Monitoring", "Air Quality Management", "Waste Management", "Health & Safety Analytics"],
        "🚗 Transportation & Fleet": ["Fleet Management System", "Vehicle Tracking", "Maintenance Scheduling", "Driver Management"]
    }
}

# Comprehensive Terms & Conditions Templates
TERMS_TEMPLATES = {
    "system_wide": {
        "title": "System-Wide Terms & Conditions",
        "content": """
        ## General Usage Terms
        By accessing and using the Alkhorayef Group Shared Services Budgeting System, you agree to comply with these terms and conditions.

        ## Data Privacy & Security
        All data entered into the system is protected under our comprehensive data protection policies in compliance with applicable regulations including GDPR and Saudi Arabian data privacy laws.

        ## Service Framework
        This system facilitates the selection and budgeting of shared services across five core departments: IT, HR, Legal, Procurement, and Facilities & Safety.

        ## User Responsibilities
        - Users are responsible for accurate data entry and compliance with company policies
        - Users must have proper authorization to commit company resources
        - All budget submissions must be reviewed and approved by appropriate management

        ## Limitation of Liability
        The shared services departments provide services in good faith and limit liability as outlined in individual service agreements.

        ## Dispute Resolution
        Any disputes regarding services or terms will be resolved through established Alkhorayef Group procedures.
        """,
        "version": "1.0",
        "effective_date": "2025-01-01"
    },
    "IT": {
        "title": "IT Shared Services Terms & Conditions",
        "content": """
        ## Software Licensing Obligations
        - All users must comply with software license terms and usage restrictions
        - License counts are monitored and enforced according to vendor agreements
        - Unauthorized software installation is strictly prohibited

        ## Data Security Requirements
        - IT services include security protocols that must be followed by all users
        - Regular security training is mandatory for all service users
        - Data backup and recovery procedures must be followed

        ## System Integration Responsibilities
        - Companies requesting IT services must provide necessary access for implementations
        - System integration requires coordination with internal IT teams
        - Testing and validation procedures must be completed before go-live

        ## Support Procedures
        - Support requests must follow established procedures and service level agreements
        - Priority levels are assigned based on business impact
        - Emergency support is available 24/7 for critical systems
        """,
        "version": "1.0",
        "effective_date": "2025-01-01"
    },
    "HR": {
        "title": "HR Shared Services Terms & Conditions", 
        "content": """
        ## Employee Data Privacy
        - All HR services comply with employment law and data privacy regulations
        - Employee consent is required for data processing activities
        - Data retention policies are strictly enforced

        ## Training Obligations
        - Companies must ensure employee participation in required training programs
        - Training completion is tracked and reported
        - Compliance training is mandatory for all employees

        ## Performance Management Participation
        - HR services require active participation in performance management processes
        - Regular feedback and reviews are required
        - Goal setting and achievement tracking is mandatory

        ## Employment Policy Compliance
        - All HR services must align with company employment policies
        - Regular policy updates and communication are required
        - Compliance monitoring and reporting is conducted regularly
        """,
        "version": "1.0",
        "effective_date": "2025-01-01"
    },
    "Legal": {
        "title": "Legal Shared Services Terms & Conditions",
        "content": """
        ## Attorney-Client Privilege
        - Legal services maintain attorney-client privilege where applicable
        - Confidential communications are protected under applicable laws
        - Privilege logs are maintained for all legal matters

        ## Conflict Disclosure
        - Companies must disclose any potential conflicts of interest
        - Regular conflict checks are performed
        - Conflict resolution procedures are in place

        ## Legal Advice Limitations
        - Legal services are provided within the scope of shared services agreements
        - External counsel may be required for specialized matters
        - Service limitations are clearly defined and communicated

        ## Document Retention
        - Legal documents must be retained according to regulatory requirements
        - Document destruction schedules are strictly followed
        - Electronic discovery procedures are in place
        """,
        "version": "1.0",
        "effective_date": "2025-01-01"
    },
    "Procurement": {
        "title": "Procurement Shared Services Terms & Conditions",
        "content": """
        ## Purchase Commitments
        - Companies must honor purchase commitments made through the procurement system
        - Purchase orders are binding once approved
        - Cancellation policies are strictly enforced

        ## Supplier Compliance
        - All suppliers must meet Alkhorayef Group compliance requirements
        - Regular supplier audits and assessments are conducted
        - Non-compliant suppliers may be suspended or terminated

        ## Contract Procedures
        - Procurement contracts must follow established procedures and approval workflows
        - Contract terms are standardized where possible
        - Contract modifications require proper authorization

        ## Payment Terms
        - Payment obligations must be met according to agreed terms and conditions
        - Late payment penalties may apply
        - Dispute resolution procedures are in place for payment issues
        """,
        "version": "1.0",
        "effective_date": "2025-01-01"
    },
    "Facility_Safety": {
        "title": "Facilities & Safety Shared Services Terms & Conditions",
        "content": """
        ## Safety Compliance
        - All facility users must comply with safety protocols and procedures
        - Regular safety training is mandatory
        - Safety violations are subject to disciplinary action

        ## Facility Access Rules
        - Access to facilities is governed by security and safety protocols
        - Visitor management procedures must be followed
        - Unauthorized access is strictly prohibited

        ## Emergency Procedures
        - Users must be familiar with and follow emergency response procedures
        - Regular emergency drills are conducted
        - Emergency contact information must be kept current

        ## Environmental Compliance
        - All activities must comply with environmental regulations and policies
        - Waste management procedures must be followed
        - Environmental incidents must be reported immediately
        """,
        "version": "1.0",
        "effective_date": "2025-01-01"
    },
    "high_value_services": {
        "title": "High-Value Service Terms (>SAR 100,000)",
        "content": """
        ## Minimum Commitment Terms
        - Services exceeding SAR 100,000 annually require minimum commitment periods
        - Early termination may result in penalties
        - Contract terms are non-negotiable without executive approval

        ## Service Level Agreements
        - Enhanced SLAs apply to high-value services
        - Performance standards are strictly monitored
        - Remediation procedures are in place for service failures

        ## Implementation Terms
        - Dedicated project management is provided for high-value implementations
        - Regular status reporting and milestone reviews are required
        - Acceptance criteria must be defined and agreed upon
        """,
        "version": "1.0",
        "effective_date": "2025-01-01"
    },
    "budget_submission": {
        "title": "Budget Submission Legal Framework",
        "content": """
        ## Authority Confirmation
        By submitting this budget, I confirm that I have the proper authority to commit company resources for the selected services and budget amounts.

        ## Budget Accuracy Representations
        I warrant that all budget information provided is accurate to the best of my knowledge and has been prepared in accordance with company policies.

        ## Funding Commitments
        My company commits to funding the approved services as outlined in this submission, subject to normal budget approval processes.

        ## Change Management
        Any modifications to approved budgets and services must follow established change management procedures and may require additional approvals.

        ## Contract Formation
        I understand that budget approval creates binding service obligations and may result in formal service agreements between my company and the shared services departments.

        ## Legal Implications
        This budget submission constitutes a formal request for services and may have legal and financial implications for my company.
        """,
        "version": "1.0",
        "effective_date": "2025-01-01"
    }
}

# Workflow Steps
WORKFLOW_STEPS = [
    {'key': 'company_info', 'title': 'Company Info', 'icon': '🏢', 'description': 'Company and contact information'},
    {'key': 'terms_system', 'title': 'System Terms', 'icon': '📋', 'description': 'System-wide terms and conditions'},
    {'key': 'department_selection', 'title': 'Department', 'icon': '🎯', 'description': 'Select shared service department'},
    {'key': 'terms_department', 'title': 'Dept Terms', 'icon': '⚖️', 'description': 'Department-specific terms'},
    {'key': 'services', 'title': 'Services', 'icon': '🛍️', 'description': 'Select operational services'},
    {'key': 'support', 'title': 'Support', 'icon': '🛠️', 'description': 'Choose support package'},
    {'key': 'projects', 'title': 'Projects', 'icon': '🚀', 'description': 'Define implementation projects'},
    {'key': 'terms_submission', 'title': 'Final Terms', 'icon': '✍️', 'description': 'Budget submission terms'},
    {'key': 'summary', 'title': 'Summary', 'icon': '📊', 'description': 'Review and submit'}
]

# ==================== ENHANCED CSS STYLING ====================

st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e40af, #3b82f6);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .admin-header {
        background: linear-gradient(90deg, #dc2626, #ef4444);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3);
    }
    
    .department-card {
        background: white;
        border: 3px solid #e5e7eb;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 0.5rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        position: relative;
        min-height: 220px;
    }
    
    .department-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .department-card.selected {
        border-color: #dc2626;
        background: linear-gradient(135deg, #fef2f2 0%, #fecaca 100%);
        box-shadow: 0 8px 25px rgba(220, 38, 38, 0.25);
    }
    
    .step-indicator {
        display: flex;
        justify-content: space-between;
        margin: 2rem 0;
        padding: 0 1rem;
        flex-wrap: wrap;
    }
    
    .step {
        display: flex;
        flex-direction: column;
        align-items: center;
        flex: 1;
        position: relative;
        min-width: 100px;
        margin: 0.5rem;
    }
    
    .step-circle {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        color: white;
        margin-bottom: 0.5rem;
        font-size: 1.2em;
    }
    
    .step-circle.completed {
        background: #10b981;
        box-shadow: 0 0 0 4px rgba(16, 185, 129, 0.2);
    }
    
    .step-circle.current {
        background: #3b82f6;
        box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.2);
        animation: pulse 2s infinite;
    }
    
    .step-circle.pending {
        background: #9ca3af;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(59, 130, 246, 0); }
        100% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0); }
    }
    
    .step-title {
        font-size: 0.8em;
        text-align: center;
        color: #374151;
        font-weight: 600;
        line-height: 1.2;
    }
    
    .terms-modal {
        background: #fef7ff;
        border: 2px solid #8b5cf6;
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem 0;
        border-left: 6px solid #8b5cf6;
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.15);
    }
    
    .terms-content {
        background: white;
        border-radius: 12px;
        padding: 2rem;
        margin: 1rem 0;
        max-height: 400px;
        overflow-y: auto;
        border: 1px solid #e5e7eb;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .license-card {
        background: #f0f9ff;
        border: 2px solid #0ea5e9;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 6px solid #0ea5e9;
    }
    
    .license-constraint {
        background: #fef2f2;
        border: 2px solid #f87171;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        color: #991b1b;
        font-weight: 600;
    }
    
    .license-available {
        background: #f0fdf4;
        border: 2px solid #22c55e;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        color: #15803d;
        font-weight: 600;
    }
    
    .service-card {
        background: white;
        border: 2px solid #e5e7eb;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .service-card:hover {
        border-color: #3b82f6;
        box-shadow: 0 4px 16px rgba(59, 130, 246, 0.15);
        transform: translateY(-2px);
    }
    
    .cost-display {
        background: #f0f9ff;
        border: 2px solid #0ea5e9;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        margin: 1rem 0;
        font-weight: bold;
    }
    
    .total-budget {
        background: linear-gradient(45deg, #dc2626, #ef4444);
        color: white;
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        font-size: 1.2em;
        font-weight: bold;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(220, 38, 38, 0.3);
    }
    
    .progress-bar {
        background: #f3f4f6;
        border-radius: 10px;
        height: 8px;
        margin: 1rem 0;
        overflow: hidden;
    }
    
    .progress-fill {
        background: linear-gradient(90deg, #10b981, #34d399);
        height: 100%;
        border-radius: 10px;
        transition: width 0.3s ease;
    }
    
    .success-message {
        background: #f0fdf4;
        border: 2px solid #10b981;
        color: #065f46;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        font-weight: 600;
    }
    
    .warning-message {
        background: #fffbeb;
        border: 2px solid #f59e0b;
        color: #92400e;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        font-weight: 600;
    }
    
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        border: 2px solid #e5e7eb;
        margin: 0.5rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# ==================== SESSION STATE INITIALIZATION ====================

def initialize_session_state():
    """Initialize all session state variables"""
    
    # Core application state
    if 'app_mode' not in st.session_state:
        st.session_state.app_mode = 'client'
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 'company_info'
    if 'selected_department' not in st.session_state:
        st.session_state.selected_department = None
    
    # User and company information
    if 'company_info' not in st.session_state:
        st.session_state.company_info = {}
    
    # Enhanced Terms & Conditions tracking
    if 'terms_accepted' not in st.session_state:
        st.session_state.terms_accepted = {
            'system_wide': {'accepted': False, 'timestamp': None, 'version': None},
            'department_specific': {},
            'high_value_services': {'accepted': False, 'timestamp': None},
            'budget_submission': {'accepted': False, 'timestamp': None}
        }
    
    # Service selections by department
    if 'operational_services' not in st.session_state:
        st.session_state.operational_services = {dept: {} for dept in SHARED_SERVICE_DEPARTMENTS.keys()}
    if 'custom_services' not in st.session_state:
        st.session_state.custom_services = {dept: [] for dept in SHARED_SERVICE_DEPARTMENTS.keys()}
    if 'support_packages' not in st.session_state:
        st.session_state.support_packages = {dept: None for dept in SHARED_SERVICE_DEPARTMENTS.keys()}
    if 'support_extras' not in st.session_state:
        st.session_state.support_extras = {dept: {'support': 0, 'training': 0, 'reports': 0} for dept in SHARED_SERVICE_DEPARTMENTS.keys()}
    if 'implementation_projects' not in st.session_state:
        st.session_state.implementation_projects = {dept: [] for dept in SHARED_SERVICE_DEPARTMENTS.keys()}
    
    # Current license inventory (IT specific)
    if 'current_licenses' not in st.session_state:
        st.session_state.current_licenses = DEFAULT_LICENSE_INVENTORY.copy()
    
    # Admin authentication
    if 'admin_authenticated' not in st.session_state:
        st.session_state.admin_authenticated = False
    if 'admin_user' not in st.session_state:
        st.session_state.admin_user = None
    if 'admin_info' not in st.session_state:
        st.session_state.admin_info = {}
    
    # Admin-managed data
    if 'admin_services' not in st.session_state:
        st.session_state.admin_services = DEFAULT_SERVICES.copy()
    if 'admin_support_packages' not in st.session_state:
        st.session_state.admin_support_packages = DEFAULT_SUPPORT_PACKAGES.copy()
    if 'admin_rpa_packages' not in st.session_state:
        st.session_state.admin_rpa_packages = DEFAULT_RPA_PACKAGES.copy()
    if 'admin_project_categories' not in st.session_state:
        st.session_state.admin_project_categories = DEFAULT_PROJECT_CATEGORIES.copy()
    if 'admin_terms' not in st.session_state:
        st.session_state.admin_terms = TERMS_TEMPLATES.copy()

# ==================== AUTHENTICATION FUNCTIONS ====================

def authenticate_admin(username, password):
    """Authenticate admin user"""
    if username in ADMIN_CREDENTIALS:
        stored_password = ADMIN_CREDENTIALS[username]["password"]
        if password == stored_password:
            return True, ADMIN_CREDENTIALS[username]
    return False, None

def check_admin_access(required_department=None):
    """Check if user has admin access for the specified department"""
    if not st.session_state.get('admin_authenticated', False):
        return False
    
    admin_info = st.session_state.get('admin_info', {})
    admin_dept = admin_info.get('department', '')
    
    if admin_dept == 'ALL':  # Super admin
        return True
    
    if required_department is None:
        return True
    
    return admin_dept == required_department

# ==================== WORKFLOW MANAGEMENT ====================

def get_workflow_steps():
    """Get workflow steps"""
    return WORKFLOW_STEPS

def show_progress_indicator():
    """Show enhanced workflow progress indicator"""
    steps = get_workflow_steps()
    current_step = st.session_state.current_step
    
    # Find current step index
    current_index = next((i for i, step in enumerate(steps) if step['key'] == current_step), 0)
    
    # Create step indicator HTML
    step_html = '<div class="step-indicator">'
    
    for i, step in enumerate(steps):
        if i < current_index:
            circle_class = "completed"
            icon = "✓"
        elif i == current_index:
            circle_class = "current"
            icon = step['icon']
        else:
            circle_class = "pending"
            icon = step['icon']
        
        step_html += f'''
        <div class="step">
            <div class="step-circle {circle_class}">{icon}</div>
            <div class="step-title">{step['title']}</div>
        </div>
        '''
    
    step_html += '</div>'
    
    # Progress bar
    progress = (current_index / (len(steps) - 1)) * 100 if len(steps) > 1 else 0
    progress_html = f'''
    <div class="progress-bar">
        <div class="progress-fill" style="width: {progress}%;"></div>
    </div>
    '''
    
    st.markdown(step_html, unsafe_allow_html=True)
    st.markdown(progress_html, unsafe_allow_html=True)

def navigate_to_step(step_key):
    """Navigate to a specific step"""
    st.session_state.current_step = step_key
    st.rerun()

# ==================== TERMS & CONDITIONS FUNCTIONS ====================

def show_terms_modal(terms_type, department=None, service_name=None):
    """Show enhanced terms and conditions modal with acceptance tracking"""
    
    # Determine which terms to show
    if terms_type == 'system_wide':
        terms_data = st.session_state.admin_terms['system_wide']
        terms_key = 'system_wide'
    elif terms_type == 'department' and department:
        terms_data = st.session_state.admin_terms.get(department, {
            'title': f'{SHARED_SERVICE_DEPARTMENTS[department]["title"]} Terms',
            'content': f'Department-specific terms for {SHARED_SERVICE_DEPARTMENTS[department]["title"]} will be defined here.',
            'version': '1.0',
            'effective_date': '2025-01-01'
        })
        terms_key = department
    elif terms_type == 'high_value':
        terms_data = st.session_state.admin_terms['high_value_services']
        terms_key = 'high_value_services'
    elif terms_type == 'budget_submission':
        terms_data = st.session_state.admin_terms['budget_submission']
        terms_key = 'budget_submission'
    else:
        return False
    
    # Check if already accepted
    if terms_type == 'system_wide':
        already_accepted = st.session_state.terms_accepted['system_wide']['accepted']
    elif terms_type == 'department':
        already_accepted = st.session_state.terms_accepted['department_specific'].get(department, {}).get('accepted', False)
    elif terms_type == 'high_value':
        already_accepted = st.session_state.terms_accepted['high_value_services']['accepted']
    elif terms_type == 'budget_submission':
        already_accepted = st.session_state.terms_accepted['budget_submission']['accepted']
    else:
        already_accepted = False
    
    if already_accepted:
        st.markdown(f"""
        <div class='success-message'>
            ✅ {terms_data['title']} have been accepted. You can proceed.
        </div>
        """, unsafe_allow_html=True)
        return True
    
    # Show terms modal
    st.markdown(f"""
    <div class='terms-modal'>
        <h2>📋 {terms_data['title']}</h2>
        <p style='margin: 0.5rem 0; color: #6b7280;'>
            <strong>Version:</strong> {terms_data.get('version', '1.0')} | 
            <strong>Effective Date:</strong> {terms_data.get('effective_date', '2025-01-01')}
        </p>
        <div class='terms-content'>
            {terms_data['content'].replace(chr(10), '<br>')}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Reading progress indicator
    st.markdown("""
    <div style='background: #fef3c7; border: 1px solid #f59e0b; border-radius: 8px; padding: 1rem; margin: 1rem 0;'>
        📖 <strong>Please read the complete terms above before accepting.</strong> 
        Your acceptance will be recorded with timestamp and IP address for compliance purposes.
    </div>
    """, unsafe_allow_html=True)
    
    # Acceptance buttons
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col2:
        if st.button("❌ Decline", use_container_width=True, key=f"decline_{terms_key}"):
            st.error("You must accept the terms to continue using the system.")
            return False
    
    with col3:
        if st.button("✅ Accept Terms", use_container_width=True, type="primary", key=f"accept_{terms_key}"):
            # Record acceptance
            timestamp = datetime.now().isoformat()
            
            if terms_type == 'system_wide':
                st.session_state.terms_accepted['system_wide'] = {
                    'accepted': True,
                    'timestamp': timestamp,
                    'version': terms_data.get('version', '1.0'),
                    'ip_address': 'demo_ip'  # In production, get actual IP
                }
            elif terms_type == 'department':
                if department not in st.session_state.terms_accepted['department_specific']:
                    st.session_state.terms_accepted['department_specific'][department] = {}
                st.session_state.terms_accepted['department_specific'][department] = {
                    'accepted': True,
                    'timestamp': timestamp,
                    'version': terms_data.get('version', '1.0'),
                    'ip_address': 'demo_ip'
                }
            elif terms_type == 'high_value':
                st.session_state.terms_accepted['high_value_services'] = {
                    'accepted': True,
                    'timestamp': timestamp,
                    'version': terms_data.get('version', '1.0'),
                    'ip_address': 'demo_ip'
                }
            elif terms_type == 'budget_submission':
                st.session_state.terms_accepted['budget_submission'] = {
                    'accepted': True,
                    'timestamp': timestamp,
                    'version': terms_data.get('version', '1.0'),
                    'ip_address': 'demo_ip'
                }
            
            st.success(f"✅ Terms accepted successfully! Acceptance recorded at {timestamp}")
            return True
    
    return False

# ==================== CALCULATION FUNCTIONS ====================

def calculate_operational_total(department):
    """Calculate total operational services cost for a department"""
    total = 0
    
    # Predefined services
    for service_name, data in st.session_state.operational_services[department].items():
        if data.get('selected', False):
            total += data.get('annual_cost', 0)
    
    # Custom services
    for service in st.session_state.custom_services[department]:
        total += service.get('annual_cost', 0)
    
    return total

def calculate_support_total(department):
    """Calculate support package cost for a department"""
    package = st.session_state.support_packages[department]
    extras = st.session_state.support_extras[department]
    
    total = 0
    if package and package in st.session_state.admin_support_packages:
        total += st.session_state.admin_support_packages[package]['price']
    
    # Add extras
    total += extras.get('support', 0) * 1800
    total += extras.get('training', 0) * 5399
    total += extras.get('reports', 0) * 5399
    
    return total

def calculate_project_total(department):
    """Calculate implementation projects cost for a department"""
    return sum(project.get('budget', 0) for project in st.session_state.implementation_projects[department])

def calculate_total_budget_all_departments():
    """Calculate total budget across all departments"""
    total = 0
    for dept in SHARED_SERVICE_DEPARTMENTS.keys():
        total += calculate_operational_total(dept)
        total += calculate_support_total(dept)
        total += calculate_project_total(dept)
    return total

# ==================== ADMIN FUNCTIONS - COMPLETION ====================

def show_department_admin_dashboard(admin_dept):
    """Show department-specific admin dashboard"""
    dept_config = SHARED_SERVICE_DEPARTMENTS[admin_dept]
    
    st.markdown(f"## {dept_config['icon']} {dept_config['title']} - Department Admin")
    st.markdown(f"Manage {dept_config['title']} services, pricing, and department-specific configurations.")
    
    tabs = st.tabs(["📊 Overview", "🛠️ Services", "💰 Pricing", "📋 Terms", "📈 Analytics"])
    
    with tabs[0]:
        show_department_overview(admin_dept)
    
    with tabs[1]:
        show_department_services(admin_dept)
    
    with tabs[2]:
        show_department_pricing(admin_dept)
    
    with tabs[3]:
        show_department_terms(admin_dept)
    
    with tabs[4]:
        show_department_analytics(admin_dept)

def show_department_overview(dept):
    """Show department-specific overview"""
    dept_config = SHARED_SERVICE_DEPARTMENTS[dept]
    
    st.markdown(f"### {dept_config['title']} Department Overview")
    
    # Key metrics for this department
    services_count = len(st.session_state.admin_services[dept])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Services", services_count)
    
    with col2:
        if dept == "IT":
            st.metric("RPA Packages", len(st.session_state.admin_rpa_packages))
        else:
            st.metric("Categories", len(st.session_state.admin_project_categories[dept]))
    
    with col3:
        projects_count = len(st.session_state.implementation_projects[dept])
        st.metric("Active Projects", projects_count)
    
    with col4:
        terms_accepted = st.session_state.terms_accepted['department_specific'].get(dept, {}).get('accepted', False)
        st.metric("Terms Status", "✅" if terms_accepted else "❌")
    
    # Department-specific insights
    if dept == "IT":
        st.markdown("#### Current License Status")
        for service, details in st.session_state.current_licenses.items():
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown(f"**{service}:** {details['current_count']} licenses")
            with col2:
                status = "🔒 Locked" if not details['can_reduce'] else "🔓 Flexible"
                st.markdown(status)

def show_department_services(dept):
    """Show department services management"""
    dept_config = SHARED_SERVICE_DEPARTMENTS[dept]
    services = st.session_state.admin_services[dept]
    
    st.markdown(f"### {dept_config['title']} Services Management")
    
    # Add new service specific to this department
    with st.expander(f"➕ Add New {dept_config['title']} Service"):
        with st.form(f"add_dept_service_{dept}"):
            service_name = st.text_input("Service Name")
            description = st.text_area("Description")
            
            # Department-specific pricing
            if dept == "IT":
                price = st.number_input("Price per User/Month (SAR)", min_value=0, value=100)
                pricing_key = "price_per_user"
            elif dept == "HR":
                price = st.number_input("Price per User/Month (SAR)", min_value=0, value=75)
                pricing_key = "price_per_user"
            elif dept == "Legal":
                price = st.number_input("Price per Contract/Month (SAR)", min_value=0, value=200)
                pricing_key = "price_per_contract"
            elif dept == "Procurement":
                price = st.number_input("Price per Transaction (SAR)", min_value=0, value=50)
                pricing_key = "price_per_transaction"
            else:  # Facility_Safety
                price = st.number_input("Price per Sq Meter/Year (SAR)", min_value=0, value=25)
                pricing_key = "price_per_sq_meter"
            
            setup_cost = st.number_input("Setup Cost (SAR)", min_value=0, value=5000)
            
            if st.form_submit_button(f"Add Service"):
                if service_name and description:
                    st.session_state.admin_services[dept][service_name] = {
                        pricing_key: price,
                        'setup_cost': setup_cost,
                        'description': description
                    }
                    st.success(f"✅ Added {service_name}")
                    st.rerun()
    
    # List existing services
    if services:
        for service_name, details in services.items():
            with st.expander(f"✏️ {service_name}"):
                new_desc = st.text_area("Description", value=details['description'], 
                                       key=f"dept_desc_{dept}_{service_name}")
                
                pricing_key = next(k for k in details.keys() if k.startswith('price_per_'))
                new_price = st.number_input(f"Price", value=details[pricing_key], 
                                          min_value=0, key=f"dept_price_{dept}_{service_name}")
                new_setup = st.number_input("Setup Cost", value=details['setup_cost'], 
                                          min_value=0, key=f"dept_setup_{dept}_{service_name}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("💾 Update", key=f"dept_update_{dept}_{service_name}"):
                        st.session_state.admin_services[dept][service_name].update({
                            'description': new_desc,
                            pricing_key: new_price,
                            'setup_cost': new_setup
                        })
                        st.success(f"✅ Updated {service_name}")
                        st.rerun()
                
                with col2:
                    if st.button("🗑️ Remove", key=f"dept_remove_{dept}_{service_name}"):
                        del st.session_state.admin_services[dept][service_name]
                        st.success(f"🗑️ Removed {service_name}")
                        st.rerun()

def show_department_pricing(dept):
    """Show department pricing management"""
    dept_config = SHARED_SERVICE_DEPARTMENTS[dept]
    
    st.markdown(f"### {dept_config['title']} Pricing Management")
    
    # Show current pricing structure
    services = st.session_state.admin_services[dept]
    
    if services:
        pricing_data = []
        for service_name, details in services.items():
            pricing_key = next(k for k in details.keys() if k.startswith('price_per_'))
            unit = pricing_key.replace('price_per_', '').replace('_', ' ').title()
            
            pricing_data.append({
                'Service': service_name,
                'Unit Price (SAR)': details[pricing_key],
                'Unit Type': unit,
                'Setup Cost (SAR)': details['setup_cost']
            })
        
        df = pd.DataFrame(pricing_data)
        st.dataframe(df, use_container_width=True)
        
        # Pricing analytics
        fig = px.bar(df, x='Service', y='Unit Price (SAR)', 
                    title=f"{dept_config['title']} Service Pricing")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info(f"No services configured for {dept_config['title']} yet.")

def show_department_terms(dept):
    """Show department terms management"""
    dept_config = SHARED_SERVICE_DEPARTMENTS[dept]
    
    st.markdown(f"### {dept_config['title']} Terms & Conditions")
    
    # Get department-specific terms
    terms_data = st.session_state.admin_terms.get(dept, {
        'title': f'{dept_config["title"]} Terms & Conditions',
        'content': f'Department-specific terms for {dept_config["title"]} services.',
        'version': '1.0',
        'effective_date': '2025-01-01'
    })
    
    # Edit terms
    new_title = st.text_input("Terms Title", value=terms_data['title'])
    new_content = st.text_area("Terms Content", value=terms_data['content'], height=300)
    
    col1, col2 = st.columns(2)
    with col1:
        new_version = st.text_input("Version", value=terms_data.get('version', '1.0'))
    with col2:
        new_date = st.date_input("Effective Date")
    
    if st.button("💾 Update Department Terms", type="primary"):
        st.session_state.admin_terms[dept] = {
            'title': new_title,
            'content': new_content,
            'version': new_version,
            'effective_date': new_date.strftime("%Y-%m-%d")
        }
        st.success(f"✅ Updated {dept_config['title']} terms")
        st.rerun()
    
    # Preview terms
    if st.button("👁️ Preview Terms"):
        st.markdown(f"**Preview: {new_title}**")
        st.markdown(new_content)

def show_department_analytics(dept):
    """Show department analytics"""
    dept_config = SHARED_SERVICE_DEPARTMENTS[dept]
    
    st.markdown(f"### {dept_config['title']} Analytics")
    
    # Service usage simulation
    services = list(st.session_state.admin_services[dept].keys())
    if services:
        # Simulate usage data
        usage_data = {service: 50 + (hash(service) % 50) for service in services}
        
        fig = px.bar(
            x=list(usage_data.keys()),
            y=list(usage_data.values()),
            title=f"{dept_config['title']} Service Usage (Simulated)",
            labels={'y': 'Usage %', 'x': 'Service'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Budget projections
    operational_total = calculate_operational_total(dept)
    support_total = calculate_support_total(dept)
    project_total = calculate_project_total(dept)
    
    if operational_total + support_total + project_total > 0:
        budget_data = {
            'Category': ['Operational', 'Support', 'Projects'],
            'Amount': [operational_total, support_total, project_total]
        }
        
        fig = px.pie(
            values=budget_data['Amount'],
            names=budget_data['Category'],
            title=f"{dept_config['title']} Budget Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No budget data available yet.")

# ==================== MAIN APPLICATION LOGIC ====================

def main():
    """Main application function"""
    initialize_session_state()
    
    # Show header and sidebar
    show_header()
    show_sidebar()
    
    # Route based on app mode
    if st.session_state.app_mode == 'admin':
        if not st.session_state.get('admin_authenticated', False):
            show_admin_login()
        else:
            show_admin_dashboard()
    else:
        # Client mode - show progress and handle workflow
        show_progress_indicator()
        
        # Route to appropriate step
        current_step = st.session_state.current_step
        
        if current_step == 'company_info':
            show_company_info_step()
        elif current_step == 'terms_system':
            show_system_terms_step()
        elif current_step == 'department_selection':
            show_department_selection_step()
        elif current_step == 'terms_department':
            show_department_terms_step()
        elif current_step == 'services':
            show_services_step()
        elif current_step == 'support':
            show_support_step()
        elif current_step == 'projects':
            show_projects_step()
        elif current_step == 'terms_submission':
            show_terms_submission_step()
        elif current_step == 'summary':
            show_summary_step()

# ==================== REMAINING HELPER FUNCTIONS ====================

def show_header():
    """Show application header"""
    app_mode = st.session_state.get('app_mode', 'client')
    
    if app_mode == 'admin':
        admin_info = st.session_state.get('admin_info', {})
        admin_name = admin_info.get('name', 'Administrator')
        
        st.markdown(f"""
        <div class='admin-header'>
            <h1>🔧 Alkhorayef Group - Admin Panel</h1>
            <h2>2025 Shared Services Content Management</h2>
            <p><strong>Administrator:</strong> {admin_name} | <strong>Mode:</strong> Department Head Panel</p>
            <p>Manage services, pricing, terms & conditions, and user compliance</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class='main-header'>
            <h1>💼 Alkhorayef Group</h1>
            <h2>2025 Multi-Department Shared Services Budgeting System</h2>
            <p><strong>Budget Year:</strong> 2025 | <strong>Version:</strong> 4.0 | <strong>Environment:</strong> Demo System</p>
            <p>Complete Terms & Conditions Framework | All 5 Departments | Current License Management</p>
        </div>
        """, unsafe_allow_html=True)

def show_sidebar():
    """Show enhanced sidebar with navigation and summary"""
    with st.sidebar:
        # Mode switcher
        st.markdown("### 🔄 Application Mode")
        
        current_mode = st.session_state.get('app_mode', 'client')
        
        if current_mode == 'client':
            if st.button("🔧 Switch to Admin Mode", use_container_width=True, type="secondary"):
                st.session_state.app_mode = 'admin'
                st.session_state.admin_authenticated = False
                st.rerun()
        else:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("👥 Client Mode", use_container_width=True):
                    st.session_state.app_mode = 'client'
                    st.rerun()
            with col2:
                if st.button("🚪 Logout", use_container_width=True, type="secondary"):
                    st.session_state.admin_authenticated = False
                    st.session_state.app_mode = 'client'
                    st.rerun()
        
        st.markdown("---")
        
        if current_mode == 'client':
            show_client_sidebar()
        else:
            show_admin_sidebar()

def show_client_sidebar():
    """Show client mode sidebar"""
    st.markdown("### 🏢 Company Information")
    
    # Company info summary
    company_info = st.session_state.company_info
    if company_info:
        st.markdown(f"""
        **Company:** {company_info.get('company', 'Not selected')}  
        **Department:** {company_info.get('department', 'Not selected')}  
        **Contact:** {company_info.get('contact_person', 'Not provided')}
        """)
    else:
        st.info("Please complete company information")
    
    # Selected department info
    if st.session_state.selected_department:
        dept_config = SHARED_SERVICE_DEPARTMENTS[st.session_state.selected_department]
        st.markdown(f"""
        **Selected Service:**  
        {dept_config['icon']} {dept_config['title']}
        """)
        
        # Terms acceptance status
        st.markdown("### ✅ Terms Status")
        
        # System terms
        system_accepted = st.session_state.terms_accepted['system_wide']['accepted']
        system_status = "✅ Accepted" if system_accepted else "❌ Pending"
        st.markdown(f"**System Terms:** {system_status}")
        
        # Department terms
        dept_accepted = st.session_state.terms_accepted['department_specific'].get(st.session_state.selected_department, {}).get('accepted', False)
        dept_status = "✅ Accepted" if dept_accepted else "❌ Pending"
        st.markdown(f"**{dept_config['title']} Terms:** {dept_status}")
    
    st.markdown("---")
    
    # Budget summary
    if st.session_state.selected_department:
        show_budget_summary()
    
    # Quick navigation
    st.markdown("### 🧭 Quick Navigation")
    steps = get_workflow_steps()
    
    for step in steps:
        # Check if step is accessible
        step_accessible = True
        if step['key'] == 'terms_department' and not st.session_state.terms_accepted['system_wide']['accepted']:
            step_accessible = False
        elif step['key'] in ['services', 'support', 'projects'] and not st.session_state.selected_department:
            step_accessible = False
        
        button_type = "primary" if step['key'] == st.session_state.current_step else "secondary"
        disabled = not step_accessible
        
        if st.button(f"{step['icon']} {step['title']}", 
                    key=f"nav_{step['key']}", 
                    use_container_width=True,
                    type=button_type,
                    disabled=disabled,
                    help=step['description']):
            navigate_to_step(step['key'])

def show_admin_sidebar():
    """Show admin mode sidebar"""
    if st.session_state.get('admin_authenticated', False):
        admin_info = st.session_state.get('admin_info', {})
        st.markdown(f"""
        **🔧 Admin Panel**  
        **User:** {admin_info.get('name', 'Admin')}  
        **Department:** {admin_info.get('department', 'N/A')}  
        **Access Level:** Department Head
        """)
        
        st.markdown("### 📊 System Statistics")
        total_services = sum(len(services) for services in st.session_state.admin_services.values())
        st.metric("Total Services", total_services)
        st.metric("Support Packages", len(st.session_state.admin_support_packages))
        st.metric("Departments", len(SHARED_SERVICE_DEPARTMENTS))
        
        # Terms acceptance statistics
        st.markdown("### 📋 Terms Compliance")
        total_system_accepted = 1 if st.session_state.terms_accepted['system_wide']['accepted'] else 0
        total_dept_accepted = len([d for d in st.session_state.terms_accepted['department_specific'].values() if d.get('accepted', False)])
        
        st.metric("System Terms", total_system_accepted, "Accepted")
        st.metric("Dept Terms", total_dept_accepted, f"of {len(SHARED_SERVICE_DEPARTMENTS)}")
        
    else:
        st.markdown("**🔐 Admin Access Required**")
        st.info("Please log in with Department Head credentials")

def show_budget_summary():
    """Show enhanced budget summary in sidebar"""
    st.markdown("### 💰 Budget Summary")
    
    dept = st.session_state.selected_department
    if not dept:
        return
    
    # Calculate totals for current department
    operational_total = calculate_operational_total(dept)
    support_total = calculate_support_total(dept)
    project_total = calculate_project_total(dept)
    total_budget = operational_total + support_total + project_total
    
    if total_budget > 0:
        st.markdown(f"""
        **Operational:** SAR {operational_total:,.0f}  
        **Support:** SAR {support_total:,.0f}  
        **Projects:** SAR {project_total:,.0f}  
        **Total:** SAR {total_budget:,.0f}
        """)
        
        # Budget distribution chart
        if operational_total > 0 or support_total > 0 or project_total > 0:
            fig = px.pie(
                values=[operational_total, support_total, project_total],
                names=['Operational', 'Support', 'Projects'],
                title=f"{SHARED_SERVICE_DEPARTMENTS[dept]['title']} Budget"
            )
            fig.update_layout(height=250, margin=dict(t=40, b=0, l=0, r=0))
            st.plotly_chart(fig, use_container_width=True)
            
        # High-value service indicator
        if total_budget > 100000:
            st.markdown("""
            <div class='warning-message'>
                ⚠️ High-Value Service: Additional terms required for budgets >SAR 100,000
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No services selected yet")

# ==================== STEP IMPLEMENTATIONS - PLACEHOLDERS ====================

def show_company_info_step():
    """Step 1: Enhanced Company Information Collection"""
    st.markdown("## 🏢 Company & Contact Information")
    st.markdown("Please provide your company and contact details to begin the shared services selection process.")
    
    with st.form("company_info_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            company = st.selectbox("Select Your Company", options=ALKHORAYEF_COMPANIES)
            department = st.selectbox("Your Department", options=COMPANY_DEPARTMENTS)
        
        with col2:
            contact_person = st.text_input("Contact Person Name", placeholder="Your full name")
            email = st.text_input("Email Address", placeholder="your.email@alkhorayef.com")
        
        # Additional fields for enhanced tracking
        st.markdown("#### Additional Information")
        col3, col4 = st.columns(2)
        
        with col3:
            phone = st.text_input("Phone Number", placeholder="+966-XXX-XXXX")
            position = st.text_input("Position/Title", placeholder="Your job title")
        
        with col4:
            budget_authority = st.selectbox("Budget Authority Level", 
                                          ["Department Head", "Finance Manager", "Executive", "Manager", "Other"])
            employee_count = st.number_input("Number of Employees in Your Department", min_value=1, value=50)
        
        submitted = st.form_submit_button("Continue to System Terms & Conditions", type="primary", use_container_width=True)
        
        if submitted:
            if company and department and contact_person and email:
                st.session_state.company_info = {
                    'company': company,
                    'department': department,
                    'contact_person': contact_person,
                    'email': email,
                    'phone': phone,
                    'position': position,
                    'budget_authority': budget_authority,
                    'employee_count': employee_count,
                    'date': datetime.now().strftime("%Y-%m-%d"),
                    'session_id': str(uuid.uuid4())
                }
                navigate_to_step('terms_system')
            else:
                st.error("Please fill in all required fields (Company, Department, Contact Person, Email).")

def show_system_terms_step():
    """Step 2: System-wide Terms & Conditions"""
    st.markdown("## 📋 System Terms & Conditions")
    st.markdown("Before proceeding, please review and accept our system-wide terms and conditions.")
    
    if not st.session_state.terms_accepted['system_wide']['accepted']:
        accepted = show_terms_modal('system_wide')
        if accepted:
            navigate_to_step('department_selection')
    else:
        st.markdown("""
        <div class='success-message'>
            ✅ System terms have been accepted. You can proceed to department selection.
        </div>
        """, unsafe_allow_html=True)
        
        # Show acceptance details
        acceptance_data = st.session_state.terms_accepted['system_wide']
        st.info(f"Accepted on: {acceptance_data.get('timestamp', 'Unknown')} | Version: {acceptance_data.get('version', '1.0')}")
        
        if st.button("Continue to Department Selection", type="primary", use_container_width=True):
            navigate_to_step('department_selection')

def show_department_selection_step():
    """Step 3: Enhanced Shared Service Department Selection"""
    st.markdown("## 🎯 Select Shared Service Department")
    st.markdown("Choose the shared service department for which you want to create a budget.")
    
    # Show all 5 departments
    cols = st.columns(len(SHARED_SERVICE_DEPARTMENTS))
    
    for i, (dept_key, dept_config) in enumerate(SHARED_SERVICE_DEPARTMENTS.items()):
        with cols[i]:
            # Check if department has selections
            has_selections = (
                len(st.session_state.operational_services[dept_key]) > 0 or
                len(st.session_state.custom_services[dept_key]) > 0 or
                st.session_state.support_packages[dept_key] is not None or
                len(st.session_state.implementation_projects[dept_key]) > 0
            )
            
            # Calculate budget for this department
            dept_budget = (calculate_operational_total(dept_key) + 
                          calculate_support_total(dept_key) + 
                          calculate_project_total(dept_key))
            
            st.markdown(f"""
            <div class='department-card {"selected" if st.session_state.selected_department == dept_key else ""}' 
                 style='border-color: {dept_config["color"]}; min-height: 240px;'>
                <h1 style='margin: 0; color: {dept_config["color"]}; font-size: 3.5em;'>{dept_config["icon"]}</h1>
                <h3 style='margin: 0.5rem 0; color: #1f2937; font-size: 1.1em;'>{dept_config["title"]}</h3>
                <p style='margin: 0.5rem 0; color: #6b7280; font-size: 0.85em; line-height: 1.4;'>{dept_config["description"]}</p>
                {f'<div style="margin-top: 1rem; padding: 0.5rem; background: {dept_config["color"]}20; border-radius: 8px; color: {dept_config["color"]}; font-weight: 600; font-size: 0.8em;">✓ Budget: SAR {dept_budget:,.0f}</div>' if has_selections else ''}
                {f'<div style="position: absolute; top: 10px; right: 10px; background: #10b981; color: white; padding: 0.25rem 0.5rem; border-radius: 12px; font-size: 0.7rem; font-weight: 600;">✓ Active</div>' if has_selections else ''}
            </div>
            """, unsafe_allow_html=True)
            
            button_text = f"Continue with {dept_config['title']}" if has_selections else f"Select {dept_config['title']}"
            button_type = "secondary" if has_selections else "primary"
            
            if st.button(button_text, key=f"select_{dept_key}", use_container_width=True, type=button_type):
                st.session_state.selected_department = dept_key
                # Check if department-specific terms are accepted
                if not st.session_state.terms_accepted['department_specific'].get(dept_key, {}).get('accepted', False):
                    navigate_to_step('terms_department')
                else:
                    navigate_to_step('services')

def show_department_terms_step():
    """Step 4: Department-specific Terms & Conditions"""
    if not st.session_state.selected_department:
        navigate_to_step('department_selection')
        return
    
    dept_config = SHARED_SERVICE_DEPARTMENTS[st.session_state.selected_department]
    
    st.markdown(f"## ⚖️ {dept_config['title']} Terms & Conditions")
    st.markdown(f"Please review the terms specific to {dept_config['title']} shared services.")
    
    if not st.session_state.terms_accepted['department_specific'].get(st.session_state.selected_department, {}).get('accepted', False):
        accepted = show_terms_modal('department', st.session_state.selected_department)
        if accepted:
            navigate_to_step('services')
    else:
        st.markdown(f"""
        <div class='success-message'>
            ✅ {dept_config['title']} terms have been accepted. You can proceed to service selection.
        </div>
        """, unsafe_allow_html=True)
        
        # Show acceptance details
        acceptance_data = st.session_state.terms_accepted['department_specific'][st.session_state.selected_department]
        st.info(f"Accepted on: {acceptance_data.get('timestamp', 'Unknown')} | Version: {acceptance_data.get('version', '1.0')}")
        
        if st.button("Continue to Service Selection", type="primary", use_container_width=True):
            navigate_to_step('services')

def show_services_step():
    """Step 5: Services Selection (Simplified)"""
    if not st.session_state.selected_department:
        navigate_to_step('department_selection')
        return
    
    dept = st.session_state.selected_department
    dept_config = SHARED_SERVICE_DEPARTMENTS[dept]
    
    st.markdown(f"## 🛍️ {dept_config['title']} - Service Selection")
    st.markdown("Select the services you need. This is a simplified demo version.")
    
    # Show simplified service selection
    services = st.session_state.admin_services[dept]
    
    for service_name, details in services.items():
        with st.expander(f"{service_name} - SAR {details.get('price_per_user', 100)}/month"):
            st.markdown(details['description'])
            
            selected = st.checkbox(f"Include {service_name}", key=f"service_{service_name}")
            
            if selected:
                quantity = st.number_input("Quantity", min_value=1, value=10, key=f"qty_{service_name}")
                
                # Simple cost calculation
                pricing_key = next(k for k in details.keys() if k.startswith('price_per_'))
                monthly_cost = details[pricing_key] * quantity
                annual_cost = monthly_cost * 12 + details['setup_cost']
                
                st.info(f"Annual Cost: SAR {annual_cost:,.0f}")
                
                # Store in session state
                service_key = service_name.replace(' ', '_').lower()
                st.session_state.operational_services[dept][service_key] = {
                    'selected': True,
                    'quantity': quantity,
                    'annual_cost': annual_cost
                }
    
    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back", use_container_width=True):
            navigate_to_step('terms_department')
    with col2:
        if st.button("Continue to Support →", type="primary", use_container_width=True):
            navigate_to_step('support')

def show_support_step():
    """Step 6: Support Package Selection (Simplified)"""
    if not st.session_state.selected_department:
        navigate_to_step('department_selection')
        return
    
    dept = st.session_state.selected_department
    dept_config = SHARED_SERVICE_DEPARTMENTS[dept]
    
    st.markdown(f"## 🛠️ {dept_config['title']} - Support Package")
    
    # Show support packages
    packages = st.session_state.admin_support_packages
    available_packages = {name: details for name, details in packages.items() 
                         if dept in details.get('departments', [])}
    
    selected_package = st.selectbox("Choose Support Package", 
                                   options=['None'] + list(available_packages.keys()))
    
    if selected_package != 'None':
        st.session_state.support_packages[dept] = selected_package
        package_details = available_packages[selected_package]
        
        st.markdown(f"""
        **{selected_package} Package**
        - **Price:** SAR {package_details['price']:,.0f}
        - **Support Requests:** {package_details['support_requests']}
        - **Training:** {package_details['training']} sessions
        - **Reports:** {package_details['reports']}
        - **Description:** {package_details['description']}
        """)
    
    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Services", use_container_width=True):
            navigate_to_step('services')
    with col2:
        if st.button("Continue to Projects →", type="primary", use_container_width=True):
            navigate_to_step('projects')

def show_projects_step():
    """Step 7: Projects (Simplified)"""
    if not st.session_state.selected_department:
        navigate_to_step('department_selection')
        return
    
    dept = st.session_state.selected_department
    dept_config = SHARED_SERVICE_DEPARTMENTS[dept]
    
    st.markdown(f"## 🚀 {dept_config['title']} - Implementation Projects")
    
    # Simple project addition
    with st.form("add_project"):
        project_name = st.text_input("Project Name")
        project_budget = st.number_input("Budget (SAR)", min_value=0, value=100000)
        
        if st.form_submit_button("Add Project"):
            if project_name:
                project = {
                    'name': project_name,
                    'budget': project_budget,
                    'description': f"Implementation project for {dept_config['title']}"
                }
                st.session_state.implementation_projects[dept].append(project)
                st.success(f"Added project: {project_name}")
    
    # Show current projects
    if st.session_state.implementation_projects[dept]:
        st.markdown("### Current Projects")
        for i, project in enumerate(st.session_state.implementation_projects[dept]):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{project['name']}** - SAR {project['budget']:,.0f}")
            with col2:
                if st.button("Remove", key=f"remove_proj_{i}"):
                    st.session_state.implementation_projects[dept].pop(i)
                    st.rerun()
    
    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Support", use_container_width=True):
            navigate_to_step('support')
    with col2:
        if st.button("Continue to Final Terms →", type="primary", use_container_width=True):
            navigate_to_step('terms_submission')

def show_terms_submission_step():
    """Step 8: Final Terms"""
    if not st.session_state.selected_department:
        navigate_to_step('department_selection')
        return
    
    dept = st.session_state.selected_department
    total_budget = calculate_operational_total(dept) + calculate_support_total(dept) + calculate_project_total(dept)
    
    st.markdown("## ✍️ Final Terms & Conditions")
    
    # High-value service terms if needed
    if total_budget > 100000:
        st.markdown("### ⚠️ High-Value Service Terms")
        if not st.session_state.terms_accepted['high_value_services']['accepted']:
            show_terms_modal('high_value')
        else:
            st.success("✅ High-value service terms accepted")
    
    # Budget submission terms
    st.markdown("### 📋 Budget Submission Terms")
    if not st.session_state.terms_accepted['budget_submission']['accepted']:
        accepted = show_terms_modal('budget_submission')
        if accepted:
            navigate_to_step('summary')
    else:
        st.success("✅ Budget submission terms accepted")
        if st.button("Continue to Summary", type="primary", use_container_width=True):
            navigate_to_step('summary')

def show_summary_step():
    """Step 9: Final Summary"""
    if not st.session_state.selected_department:
        navigate_to_step('department_selection')
        return
    
    dept = st.session_state.selected_department
    dept_config = SHARED_SERVICE_DEPARTMENTS[dept]
    
    st.markdown(f"## 📊 {dept_config['title']} - Budget Summary")
    
    # Calculate totals
    operational_total = calculate_operational_total(dept)
    support_total = calculate_support_total(dept)
    project_total = calculate_project_total(dept)
    total_budget = operational_total + support_total + project_total
    
    # Show summary
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Operational Services", f"SAR {operational_total:,.0f}")
    with col2:
        st.metric("Support Package", f"SAR {support_total:,.0f}")
    with col3:
        st.metric("Implementation Projects", f"SAR {project_total:,.0f}")
    with col4:
        st.markdown(f"""
        <div class='total-budget'>
            💰 Total Budget<br>
            <span style='font-size: 1.8em'>SAR {total_budget:,.0f}</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Final submission
    if st.button("🚀 Submit Budget Request", type="primary", use_container_width=True):
        reference_id = f"ALK-{dept[:3].upper()}-2025-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        st.balloons()
        st.success(f"""
        ✅ **Budget Successfully Submitted!**
        
        **Reference ID:** {reference_id}
        
        **Total Budget:** SAR {total_budget:,.0f}
        
        Your budget request has been submitted for {dept_config['title']} approval.
        """)

# ==================== ADMIN DASHBOARD COMPLETION ====================

def show_admin_login():
    """Show enhanced admin login interface"""
    st.markdown("""
    <div style='max-width: 500px; margin: 2rem auto; background: white; border: 2px solid #e5e7eb; border-radius: 16px; padding: 2rem; box-shadow: 0 8px 25px rgba(0,0,0,0.1);'>
        <h2 style='text-align: center; color: #dc2626; margin-bottom: 1.5rem;'>
            🔐 Department Head Access Portal
        </h2>
        <p style='text-align: center; color: #6b7280; margin-bottom: 1.5rem;'>
            Secure access for authorized Department Heads to manage shared services content, pricing, and terms & conditions.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("admin_login_form"):
        st.markdown("### Login Credentials")
        username = st.text_input("Username", placeholder="e.g., it_admin, hr_admin")
        password = st.text_input("Password", type="password")
        
        submitted = st.form_submit_button("🔓 Access Admin Panel", type="primary", use_container_width=True)
        
        if submitted:
            if username and password:
                is_valid, admin_info = authenticate_admin(username, password)
                if is_valid:
                    st.session_state.admin_authenticated = True
                    st.session_state.admin_user = username
                    st.session_state.admin_info = admin_info
                    st.success(f"✅ Welcome, {admin_info['name']}!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials.")
            else:
                st.error("Please enter both username and password.")
    
    # Enhanced demo credentials
    with st.expander("🔍 Demo Credentials"):
        st.markdown("""
        **All 5 Department Heads + Super Admin:**
        
        **IT Department Head:**
        - Username: `it_admin` / Password: `itadmin2025`
        
        **HR Department Head:**
        - Username: `hr_admin` / Password: `hradmin2025`
        
        **Legal Department Head:**
        - Username: `legal_admin` / Password: `legaladmin2025`
        
        **Procurement Department Head:**
        - Username: `procurement_admin` / Password: `procadmin2025`
        
        **Facility & Safety Department Head:**
        - Username: `facility_admin` / Password: `faciladmin2025`
        
        **Super Administrator (All Departments):**
        - Username: `super_admin` / Password: `superadmin2025`
        """)

def show_admin_dashboard():
    """Show enhanced admin dashboard"""
    admin_info = st.session_state.get('admin_info', {})
    admin_dept = admin_info.get('department', '')
    
    if admin_dept == 'ALL':
        show_super_admin_dashboard()
    else:
        show_department_admin_dashboard(admin_dept)

def show_super_admin_dashboard():
    """Show comprehensive super admin dashboard"""
    st.markdown("## 🔧 Super Administrator Dashboard")
    st.markdown("Complete system oversight and management across all departments.")
    
    tabs = st.tabs(["📊 Overview", "🛠️ Services", "📋 Terms", "👥 Users", "📈 Analytics"])
    
    with tabs[0]:
        show_admin_overview()
    
    with tabs[1]:
        show_services_management()
    
    with tabs[2]:
        show_terms_management()
    
    with tabs[3]:
        show_user_management()
    
    with tabs[4]:
        show_admin_analytics()

def show_admin_overview():
    """Show enhanced admin overview"""
    st.markdown("### 🏢 System Overview")
    
    # Key metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_services = sum(len(services) for services in st.session_state.admin_services.values())
        st.metric("Total Services", total_services)
    
    with col2:
        st.metric("Support Packages", len(st.session_state.admin_support_packages))
    
    with col3:
        st.metric("Departments", len(SHARED_SERVICE_DEPARTMENTS))
    
    with col4:
        total_terms = len(st.session_state.admin_terms)
        st.metric("Terms Documents", total_terms)
    
    with col5:
        total_admins = len(ADMIN_CREDENTIALS)
        st.metric("Admin Users", total_admins)
    
    # Services by department chart
    services_by_dept = {dept: len(services) for dept, services in st.session_state.admin_services.items()}
    
    fig = px.bar(
        x=list(services_by_dept.keys()),
        y=list(services_by_dept.values()),
        title="Services by Department",
        labels={'y': 'Number of Services', 'x': 'Department'}
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Recent activity simulation
    st.markdown("### 📈 Recent System Activity")
    st.info("🔄 This section would show real-time admin activities in a production environment.")

def show_services_management():
    """Show comprehensive services management"""
    st.markdown("### 🛠️ Services Management")
    st.info("Simplified services management - full version would include detailed service configuration.")

def show_terms_management():
    """Show comprehensive terms management"""
    st.markdown("### 📋 Terms & Conditions Management")
    st.info("Terms management interface - full version would include complete terms editing capabilities.")

def show_user_management():
    """Show user management interface"""
    st.markdown("### 👥 User & Access Management")
    st.info("User management interface - full version would include user administration features.")

def show_admin_analytics():
    """Show admin analytics dashboard"""
    st.markdown("### 📈 System Analytics")
    
    # Service usage analytics
    col1, col2 = st.columns(2)
    
    with col1:
        # Services by department
        services_data = {dept: len(services) for dept, services in st.session_state.admin_services.items()}
        fig1 = px.pie(values=list(services_data.values()), names=list(services_data.keys()), 
                     title="Services Distribution by Department")
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Support package pricing
        package_data = {name: details['price'] for name, details in st.session_state.admin_support_packages.items()}
        fig2 = px.bar(x=list(package_data.keys()), y=list(package_data.values()), 
                     title="Support Package Pricing")
        st.plotly_chart(fig2, use_container_width=True)

# ==================== RUN THE APPLICATION ====================

if __name__ == "__main__":
    main()
