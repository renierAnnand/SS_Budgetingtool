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
    """Show client mode sidebar with editing capabilities"""
    st.markdown("### 🏢 Company Information")
    
    # Company info summary with edit option
    company_info = st.session_state.company_info
    if company_info:
        st.markdown(f"""
        **Company:** {company_info.get('company', 'Not selected')}  
        **Department:** {company_info.get('department', 'Not selected')}  
        **Contact:** {company_info.get('contact_person', 'Not provided')}
        """)
        
        if st.button("✏️ Edit Company Info", key="edit_company_sidebar", use_container_width=True):
            navigate_to_step('company_info')
    else:
        st.info("Please complete company information")
    
    # Selected department info with edit option
    if st.session_state.selected_department:
        dept_config = SHARED_SERVICE_DEPARTMENTS[st.session_state.selected_department]
        st.markdown(f"""
        **Selected Service:**  
        {dept_config['icon']} {dept_config['title']}
        """)
        
        if st.button("🔄 Change Department", key="change_dept_sidebar", use_container_width=True):
            navigate_to_step('department_selection')
        
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
        
        # Quick editing options
        st.markdown("### ⚡ Quick Edit")
        
        # Check if user has selections to edit
        has_operational = len([s for s in st.session_state.operational_services[st.session_state.selected_department].values() if s.get('selected', False)]) > 0
        has_custom = len(st.session_state.custom_services[st.session_state.selected_department]) > 0
        has_support = st.session_state.support_packages[st.session_state.selected_department] is not None
        has_projects = len(st.session_state.implementation_projects[st.session_state.selected_department]) > 0
        
        if has_operational or has_custom:
            if st.button("🛍️ Edit Services", key="edit_services_sidebar", use_container_width=True):
                navigate_to_step('services')
        
        if has_support:
            if st.button("🛠️ Edit Support", key="edit_support_sidebar", use_container_width=True):
                navigate_to_step('support')
        
        if has_projects:
            if st.button("🚀 Edit Projects", key="edit_projects_sidebar", use_container_width=True):
                navigate_to_step('projects')
    
    st.markdown("---")
    
    # Budget summary
    if st.session_state.selected_department:
        show_budget_summary()
    
    # Enhanced navigation with completion indicators
    st.markdown("### 🧭 Navigation & Progress")
    steps = get_workflow_steps()
    
    for step in steps:
        # Check if step is accessible and completed
        step_accessible = True
        step_completed = False
        
        if step['key'] == 'company_info':
            step_completed = bool(st.session_state.company_info)
        elif step['key'] == 'terms_system':
            step_completed = st.session_state.terms_accepted['system_wide']['accepted']
            if not step_completed:
                step_accessible = False
        elif step['key'] == 'department_selection':
            step_completed = st.session_state.selected_department is not None
            if not st.session_state.terms_accepted['system_wide']['accepted']:
                step_accessible = False
        elif step['key'] == 'terms_department':
            if st.session_state.selected_department:
                step_completed = st.session_state.terms_accepted['department_specific'].get(st.session_state.selected_department, {}).get('accepted', False)
            if not st.session_state.selected_department:
                step_accessible = False
        elif step['key'] in ['services', 'support', 'projects', 'terms_submission', 'summary']:
            if not st.session_state.selected_department:
                step_accessible = False
            elif step['key'] == 'services':
                dept = st.session_state.selected_department
                step_completed = (len([s for s in st.session_state.operational_services[dept].values() if s.get('selected', False)]) > 0 or 
                                len(st.session_state.custom_services[dept]) > 0)
        
        # Determine button appearance
        if step['key'] == st.session_state.current_step:
            button_type = "primary"
            button_emoji = "👉"
        elif step_completed:
            button_type = "secondary"
            button_emoji = "✅"
        else:
            button_type = "secondary"
            button_emoji = step['icon']
        
        button_text = f"{button_emoji} {step['title']}"
        if step_completed and step['key'] != st.session_state.current_step:
            button_text += " ✓"
        
        if st.button(button_text, 
                    key=f"nav_{step['key']}", 
                    use_container_width=True,
                    type=button_type,
                    disabled=not step_accessible,
                    help=f"{step['description']} {'(Completed)' if step_completed else ''}"):
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
    """Show enhanced budget summary with real-time updates and editing options"""
    st.markdown("### 💰 Budget Summary")
    
    dept = st.session_state.selected_department
    if not dept:
        return
    
    # Calculate totals for current department with real-time updates
    operational_total = calculate_operational_total(dept)
    support_total = calculate_support_total(dept)
    project_total = calculate_project_total(dept)
    total_budget = operational_total + support_total + project_total
    
    if total_budget > 0:
        # Enhanced budget display with breakdown
        st.markdown(f"""
        <div style='background: #f8fafc; border: 2px solid #e5e7eb; border-radius: 12px; padding: 1rem; margin: 1rem 0;'>
            <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;'>
                <strong style='color: #374151;'>Operational Services:</strong>
                <strong style='color: {SHARED_SERVICE_DEPARTMENTS[dept]["color"]};'>SAR {operational_total:,.0f}</strong>
            </div>
            <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;'>
                <strong style='color: #374151;'>Support Package:</strong>
                <strong style='color: {SHARED_SERVICE_DEPARTMENTS[dept]["color"]};'>SAR {support_total:,.0f}</strong>
            </div>
            <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;'>
                <strong style='color: #374151;'>Projects:</strong>
                <strong style='color: {SHARED_SERVICE_DEPARTMENTS[dept]["color"]};'>SAR {project_total:,.0f}</strong>
            </div>
            <hr style='margin: 0.5rem 0; border: 1px solid #e5e7eb;'>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <strong style='color: #1f2937; font-size: 1.1em;'>Total Budget:</strong>
                <strong style='color: {SHARED_SERVICE_DEPARTMENTS[dept]["color"]}; font-size: 1.2em;'>SAR {total_budget:,.0f}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Budget distribution visualization
        if operational_total > 0 or support_total > 0 or project_total > 0:
            fig = px.pie(
                values=[operational_total, support_total, project_total],
                names=['Operational', 'Support', 'Projects'],
                title=f"{SHARED_SERVICE_DEPARTMENTS[dept]['title']} Budget",
                color_discrete_sequence=[SHARED_SERVICE_DEPARTMENTS[dept]['color'], '#10b981', '#f59e0b']
            )
            fig.update_layout(height=250, margin=dict(t=40, b=0, l=0, r=0))
            fig.update_traces(textposition='inside', textinfo='percent+value')
            st.plotly_chart(fig, use_container_width=True)
        
        # Selection summary with counts
        selections_summary = []
        
        # Count operational services
        operational_count = len([s for s in st.session_state.operational_services[dept].values() if s.get('selected', False)])
        custom_count = len(st.session_state.custom_services[dept])
        if operational_count > 0 or custom_count > 0:
            selections_summary.append(f"🛍️ {operational_count + custom_count} services")
        
        # Count support package
        if st.session_state.support_packages[dept]:
            support_extras_count = sum(st.session_state.support_extras[dept].values())
            extra_text = f" (+{support_extras_count} extras)" if support_extras_count > 0 else ""
            selections_summary.append(f"🛠️ 1 support package{extra_text}")
        
        # Count projects
        projects_count = len(st.session_state.implementation_projects[dept])
        if projects_count > 0:
            selections_summary.append(f"🚀 {projects_count} projects")
        
        if selections_summary:
            st.markdown(f"**Selections:** {' | '.join(selections_summary)}")
        
        # High-value service indicator with enhanced warning
        if total_budget > 100000:
            st.markdown(f"""
            <div class='warning-message'>
                ⚠️ <strong>High-Value Service Alert</strong><br>
                Your budget of SAR {total_budget:,.0f} exceeds SAR 100,000.<br>
                Additional high-value service terms will be required for approval.
            </div>
            """, unsafe_allow_html=True)
        
        # Budget change indicator (if we track previous values)
        if 'previous_budget' in st.session_state and st.session_state.get('previous_budget', {}).get(dept, 0) != total_budget:
            previous = st.session_state['previous_budget'].get(dept, 0)
            change = total_budget - previous
            if change != 0:
                change_color = "#10b981" if change > 0 else "#ef4444"
                change_icon = "📈" if change > 0 else "📉"
                change_text = f"+SAR {change:,.0f}" if change > 0 else f"SAR {change:,.0f}"
                st.markdown(f"""
                <div style='background: {change_color}20; border: 1px solid {change_color}; border-radius: 8px; padding: 0.5rem; margin: 0.5rem 0; color: {change_color}; font-weight: 600;'>
                    {change_icon} Budget Change: {change_text}
                </div>
                """, unsafe_allow_html=True)
        
        # Store current budget for change tracking
        if 'previous_budget' not in st.session_state:
            st.session_state.previous_budget = {}
        st.session_state.previous_budget[dept] = total_budget
        
    else:
        st.info("No services selected yet")
        
        # Quick start suggestions
        st.markdown("#### 🚀 Quick Start")
        suggestions = [
            "Select operational services to begin",
            "Choose a support package",
            "Add implementation projects"
        ]
        for suggestion in suggestions:
            st.markdown(f"• {suggestion}")

def show_summary_step():
    """Step 9: Enhanced Final Summary with Comprehensive Review and Edit Options"""
    if not st.session_state.selected_department:
        navigate_to_step('department_selection')
        return
    
    dept = st.session_state.selected_department
    dept_config = SHARED_SERVICE_DEPARTMENTS[dept]
    
    st.markdown(f"## 📊 {dept_config['title']} - Final Budget Summary & Submission")
    st.markdown("Review your complete service selection. You can still edit any section before final submission.")
    
    # Calculate totals
    operational_total = calculate_operational_total(dept)
    support_total = calculate_support_total(dept)
    project_total = calculate_project_total(dept)
    total_budget = operational_total + support_total + project_total
    
    if total_budget == 0:
        st.warning("No services have been selected. Please go back and make your selections.")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("← Back to Projects", use_container_width=True):
                navigate_to_step('projects')
        with col2:
            if st.button("🛍️ Select Services", use_container_width=True, type="primary"):
                navigate_to_step('services')
        with col3:
            if st.button("🏢 Change Department", use_container_width=True):
                navigate_to_step('department_selection')
        return
    
    # Enhanced budget overview with edit links
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class='metric-card'>
            <h3 style='margin: 0; color: #374151;'>Operational Services</h3>
            <h2 style='margin: 0.5rem 0; color: {dept_config['color']};'>SAR {operational_total:,.0f}</h2>
        </div>
        """, unsafe_allow_html=True)
        if st.button("✏️ Edit Services", key="edit_services_summary", use_container_width=True):
            navigate_to_step('services')
    
    with col2:
        st.markdown(f"""
        <div class='metric-card'>
            <h3 style='margin: 0; color: #374151;'>Support Package</h3>
            <h2 style='margin: 0.5rem 0; color: #10b981;'>SAR {support_total:,.0f}</h2>
        </div>
        """, unsafe_allow_html=True)
        if st.button("✏️ Edit Support", key="edit_support_summary", use_container_width=True):
            navigate_to_step('support')
    
    with col3:
        st.markdown(f"""
        <div class='metric-card'>
            <h3 style='margin: 0; color: #374151;'>Implementation Projects</h3>
            <h2 style='margin: 0.5rem 0; color: #f59e0b;'>SAR {project_total:,.0f}</h2>
        </div>
        """, unsafe_allow_html=True)
        if st.button("✏️ Edit Projects", key="edit_projects_summary", use_container_width=True):
            navigate_to_step('projects')
    
    with col4:
        st.markdown(f"""
        <div class='total-budget'>
            💰 Total Budget<br>
            <span style='font-size: 1.8em'>SAR {total_budget:,.0f}</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Enhanced visualizations with interactivity
    col1, col2 = st.columns(2)
    
    with col1:
        # Budget distribution pie chart
        if total_budget > 0:
            fig_pie = px.pie(
                values=[operational_total, support_total, project_total],
                names=['Operational Services', 'Support Package', 'Implementation Projects'],
                title=f"{dept_config['title']} Budget Distribution",
                color_discrete_sequence=[dept_config['color'], '#10b981', '#f59e0b']
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            fig_pie.update_layout(height=400)
            st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Monthly cash flow projection (enhanced)
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        monthly_costs = [0] * 12
        
        # Operational and support typically billed year-end
        monthly_costs[11] = operational_total + support_total
        
        # Projects distributed based on timeline
        for project in st.session_state.implementation_projects[dept]:
            timeline = project.get('timeline', 'Q4 2025')
            budget = project.get('budget', 0)
            
            if 'Q1' in timeline:
                monthly_costs[2] += budget
            elif 'Q2' in timeline:
                monthly_costs[5] += budget
            elif 'Q3' in timeline:
                monthly_costs[8] += budget
            elif 'Q4' in timeline:
                monthly_costs[11] += budget
            else:  # Multi-quarter
                monthly_amount = budget / 12
                monthly_costs = [cost + monthly_amount for cost in monthly_costs]
        
        fig_bar = px.bar(
            x=months,
            y=monthly_costs,
            title="2025 Monthly Cash Flow Projection",
            labels={'y': 'Cost (SAR)', 'x': 'Month'},
            color_discrete_sequence=[dept_config['color']]
        )
        fig_bar.update_layout(height=400)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Comprehensive detailed service breakdown with edit options
    st.markdown("### 📋 Detailed Service Selection Review")
    
    # Create tabs for different categories
    tabs = st.tabs(["🛍️ Operational Services", "🛠️ Support Package", "🚀 Implementation Projects"])
    
    with tabs[0]:
        # Operational services details with edit option
        if operational_total > 0:
            st.markdown(f"#### {dept_config['title']} Operational Services")
            
            service_total = 0
            service_count = 0
            
            for service_key, data in st.session_state.operational_services[dept].items():
                if data.get('selected', False) and data.get('annual_cost', 0) > 0:
                    service_name = service_key.replace('_', ' ').title()
                    service_total += data['annual_cost']
                    service_count += 1
                    
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        # Special display for IT services with license info
                        if dept == "IT" and 'current_count' in data:
                            current = data.get('current_count', 0)
                            requested = data.get('requested_count', 0)
                            delta = data.get('license_delta', 0)
                            delta_text = f" ({delta:+d} licenses)" if delta != 0 else " (no change)"
                            st.markdown(f"**{service_name}** - Current: {current}, Requested: {requested}{delta_text}")
                        else:
                            volume = data.get('volume', data.get('requested_count', 0))
                            st.markdown(f"**{service_name}** - Quantity: {volume}")
                    
                    with col2:
                        st.markdown(f"**SAR {data['annual_cost']:,.0f}**")
            
            # Custom services
            for service in st.session_state.custom_services[dept]:
                service_total += service['annual_cost']
                service_count += 1
                
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"**{service['name']}** (Custom) - {service['description']}")
                with col2:
                    st.markdown(f"**SAR {service['annual_cost']:,.0f}**")
            
            st.markdown(f"**Total: {service_count} services - SAR {service_total:,.0f}**")
            
            if st.button("✏️ Modify Operational Services", key="modify_services_tab", use_container_width=True):
                navigate_to_step('services')
        else:
            st.info("No operational services selected.")
            if st.button("➕ Add Operational Services", key="add_services_tab", use_container_width=True, type="primary"):
                navigate_to_step('services')
    
    with tabs[1]:
        # Support package details with edit option
        if support_total > 0:
            package_name = st.session_state.support_packages[dept]
            st.markdown(f"#### Support Package: {package_name}")
            
            base_cost = st.session_state.admin_support_packages[package_name]['price']
            extras = st.session_state.support_extras[dept]
            extra_cost = extras['support'] * 1800 + extras['training'] * 5399 + extras['reports'] * 5399
            
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"**{package_name} Package**")
                package_details = st.session_state.admin_support_packages[package_name]
                st.markdown(f"- {package_details['support_requests']} support requests")
                st.markdown(f"- {package_details['training']} training sessions")
                st.markdown(f"- {package_details['reports']} custom reports")
                st.markdown(f"- {package_details['improvement_hours']} improvement hours")
            with col2:
                st.markdown(f"**SAR {base_cost:,.0f}**")
            
            if extra_cost > 0:
                col1, col2 = st.columns([4, 1])
                with col1:
                    extra_items = []
                    if extras['support'] > 0:
                        extra_items.append(f"{extras['support']} extra support requests")
                    if extras['training'] > 0:
                        extra_items.append(f"{extras['training']} extra training sessions")
                    if extras['reports'] > 0:
                        extra_items.append(f"{extras['reports']} extra reports")
                    st.markdown(f"**Additional Services:** {', '.join(extra_items)}")
                with col2:
                    st.markdown(f"**SAR {extra_cost:,.0f}**")
            
            st.markdown(f"**Total Support: SAR {support_total:,.0f}**")
            
            if st.button("✏️ Modify Support Package", key="modify_support_tab", use_container_width=True):
                navigate_to_step('support')
        else:
            st.info("No support package selected.")
            if st.button("➕ Add Support Package", key="add_support_tab", use_container_width=True, type="primary"):
                navigate_to_step('support')
    
    with tabs[2]:
        # Implementation projects details with edit option
        if project_total > 0:
            st.markdown(f"#### Implementation Projects")
            
            projects = st.session_state.implementation_projects[dept]
            for project in projects:
                col1, col2 = st.columns([4, 1])
                with col1:
                    rpa_text = f" (RPA: {project['rpa_package']})" if project.get('rpa_package') else ""
                    st.markdown(f"**{project['name']}**{rpa_text}")
                    st.markdown(f"- Timeline: {project['timeline']}")
                    st.markdown(f"- Priority: {project['priority']}")
                    if project.get('description'):
                        st.markdown(f"- {project['description']}")
                with col2:
                    st.markdown(f"**SAR {project['budget']:,.0f}**")
            
            st.markdown(f"**Total Projects: {len(projects)} - SAR {project_total:,.0f}**")
            
            if st.button("✏️ Modify Projects", key="modify_projects_tab", use_container_width=True):
                navigate_to_step('projects')
        else:
            st.info("No implementation projects defined.")
            if st.button("➕ Add Implementation Projects", key="add_projects_tab", use_container_width=True, type="primary"):
                navigate_to_step('projects')
    
    # Terms compliance summary
    st.markdown("### ✅ Terms Compliance Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        system_status = "✅ Accepted" if st.session_state.terms_accepted['system_wide']['accepted'] else "❌ Not Accepted"
        st.markdown(f"**System Terms:** {system_status}")
    
    with col2:
        dept_status = "✅ Accepted" if st.session_state.terms_accepted['department_specific'].get(dept, {}).get('accepted', False) else "❌ Not Accepted"
        st.markdown(f"**{dept_config['title']} Terms:** {dept_status}")
    
    with col3:
        budget_status = "✅ Accepted" if st.session_state.terms_accepted['budget_submission']['accepted'] else "❌ Not Accepted"
        st.markdown(f"**Budget Submission Terms:** {budget_status}")
    
    if total_budget > 100000:
        high_value_status = "✅ Accepted" if st.session_state.terms_accepted['high_value_services']['accepted'] else "❌ Not Accepted"
        st.markdown(f"**High-Value Service Terms:** {high_value_status}")
    
    # Final submission section
    st.markdown("### 📤 Submit Your Budget Request")
    
    # Check all terms are accepted
    all_terms_accepted = (
        st.session_state.terms_accepted['system_wide']['accepted'] and
        st.session_state.terms_accepted['department_specific'].get(dept, {}).get('accepted', False) and
        st.session_state.terms_accepted['budget_submission']['accepted'] and
        (st.session_state.terms_accepted['high_value_services']['accepted'] if total_budget > 100000 else True)
    )
    
    if not all_terms_accepted:
        st.error("❌ All required terms must be accepted before submission.")
        if st.button("Review Terms & Conditions", type="primary", use_container_width=True):
            navigate_to_step('terms_submission')
        return
    
    # Action buttons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📊 Export Summary", use_container_width=True):
            st.success("📊 Excel export would generate a comprehensive budget report with all selections.")
    
    with col2:
        if st.button("💾 Save Draft", use_container_width=True):
            st.success("💾 Draft saved! You can return to edit anytime.")
    
    with col3:
        if st.button("📧 Share Summary", use_container_width=True):
            st.success("📧 Budget summary prepared for sharing with stakeholders.")
    
    with col4:
        if st.button("🚀 Submit Final Budget", type="primary", use_container_width=True):
            # Generate comprehensive submission confirmation
            company_code = st.session_state.company_info.get('company', 'ALK')
            dept_code = dept[:3].upper()
            reference_id = f"{company_code}-{dept_code}-2025-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            st.balloons()
            st.success(f"""
            ✅ **Budget Successfully Submitted!**
            
            **Reference ID:** {reference_id}
            
            **Submission Summary:**
            - Company: {st.session_state.company_info.get('company', 'N/A')}
            - Requesting Department: {st.session_state.company_info.get('department', 'N/A')}
            - Shared Service: {dept_config['title']}
            - Contact: {st.session_state.company_info.get('contact_person', 'N/A')} ({st.session_state.company_info.get('email', 'N/A')})
            - Total Budget: SAR {total_budget:,.0f}
            - Breakdown: Operational (SAR {operational_total:,.0f}) | Support (SAR {support_total:,.0f}) | Projects (SAR {project_total:,.0f})
            
            **Selection Summary:**
            - Operational Services: {len([s for s in st.session_state.operational_services[dept].values() if s.get('selected', False)]) + len(st.session_state.custom_services[dept])} services
            - Support Package: {st.session_state.support_packages[dept] or 'None'}
            - Implementation Projects: {len(st.session_state.implementation_projects[dept])} projects
            
            **Terms Compliance:**
            - System Terms: ✅ Accepted
            - {dept_config['title']} Terms: ✅ Accepted
            - Budget Submission: ✅ Accepted
            {f"- High-Value Services: ✅ Accepted" if total_budget > 100000 else ""}
            
            **Next Steps:**
            1. {dept_config['title']} team review (3-5 business days)
            2. Finance approval process (1-2 weeks)  
            3. Service implementation planning (Q4 2024)
            4. Service delivery commencement (Q1 2025)
            
            A detailed budget report has been sent to your email and the {dept_config['title']} shared services team.
            """)
            
            # Reset selections indicator for future use
            if 'previous_budget' in st.session_state:
                st.session_state.previous_budget[dept] = 0
            
            # Option to start with another department
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 Budget for Another Department", type="secondary", use_container_width=True):
                    st.session_state.selected_department = None
                    navigate_to_step('department_selection')
            with col2:
                if st.button("🏠 Return to Home", use_container_width=True):
                    for key in ['selected_department', 'current_step']:
                        if key in st.session_state:
                            del st.session_state[key]
                    st.session_state.current_step = 'company_info'
                    st.rerun()

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
    """Step 5: Enhanced Operational Services Selection with Editing Capabilities"""
    if not st.session_state.selected_department:
        navigate_to_step('department_selection')
        return
    
    dept = st.session_state.selected_department
    dept_config = SHARED_SERVICE_DEPARTMENTS[dept]
    services = st.session_state.admin_services[dept]
    
    st.markdown(f"## 🛍️ {dept_config['title']} - Operational Services")
    
    # Check if user is editing existing selections
    has_existing_selections = (
        len([s for s in st.session_state.operational_services[dept].values() if s.get('selected', False)]) > 0 or 
        len(st.session_state.custom_services[dept]) > 0
    )
    
    if has_existing_selections:
        st.markdown(f"""
        <div class='success-message'>
            ✅ You have existing service selections. You can modify, add more services, or remove selections below.
        </div>
        """, unsafe_allow_html=True)
        
        # Show current selections summary
        show_current_services_summary(dept)
    else:
        st.markdown(f"Select the operational services you need for {dept_config['title']}.")
    
    # Show current license inventory for IT department
    if dept == "IT":
        show_license_inventory()
    
    # Service selection with editing capabilities
    if dept == "IT":
        show_it_services_with_editing(dept)
    else:
        show_general_services_with_editing(dept)
    
    # Enhanced custom services section with editing
    show_custom_services_section_with_editing(dept)
    
    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Department Terms", use_container_width=True):
            navigate_to_step('terms_department')
    with col2:
        if st.button("Continue to Support Packages →", type="primary", use_container_width=True):
            navigate_to_step('support')

def show_current_services_summary(dept):
    """Show summary of currently selected services with quick remove options"""
    st.markdown("### 📋 Current Service Selections")
    
    # Operational services
    selected_services = {k: v for k, v in st.session_state.operational_services[dept].items() if v.get('selected', False)}
    
    if selected_services:
        st.markdown("#### Selected Standard Services")
        for service_key, data in selected_services.items():
            service_name = service_key.replace('_', ' ').title()
            
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                if dept == "IT" and 'current_count' in data:
                    current = data.get('current_count', 0)
                    requested = data.get('requested_count', 0)
                    delta = data.get('license_delta', 0)
                    delta_text = f" ({delta:+d} licenses)" if delta != 0 else " (no change)"
                    st.markdown(f"**{service_name}** - Current: {current}, Requested: {requested}{delta_text}")
                else:
                    volume = data.get('volume', data.get('requested_count', 0))
                    st.markdown(f"**{service_name}** - Quantity: {volume}")
            
            with col2:
                st.markdown(f"**SAR {data.get('annual_cost', 0):,.0f}**")
            
            with col3:
                if st.button("🗑️ Remove", key=f"remove_service_{service_key}", use_container_width=True):
                    st.session_state.operational_services[dept][service_key] = {
                        'selected': False,
                        'volume': 0,
                        'requested_count': 0,
                        'annual_cost': 0
                    }
                    st.success(f"Removed {service_name}")
                    st.rerun()
    
    # Custom services
    if st.session_state.custom_services[dept]:
        st.markdown("#### Custom Services")
        for i, service in enumerate(st.session_state.custom_services[dept]):
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.markdown(f"**{service['name']}** - {service['description']}")
            
            with col2:
                st.markdown(f"**SAR {service.get('annual_cost', 0):,.0f}**")
            
            with col3:
                if st.button("🗑️ Remove", key=f"remove_custom_{i}", use_container_width=True):
                    st.session_state.custom_services[dept].pop(i)
                    st.success(f"Removed {service['name']}")
                    st.rerun()
    
    st.markdown("---")

def show_it_services_with_editing(dept):
    """Show IT services with comprehensive editing capabilities"""
    st.markdown("### 💻 IT Services - Add or Modify Selections")
    
    services = st.session_state.admin_services["IT"]
    
    # Add expand/collapse for better UX
    show_all = st.checkbox("🔍 Show all available services", value=False)
    
    col1, col2 = st.columns(2)
    service_items = list(services.items())
    
    for i, (service_name, details) in enumerate(service_items):
        col = col1 if i % 2 == 0 else col2
        
        with col:
            service_key = service_name.replace(' ', '_').lower()
            
            # Check if this service has current licenses
            current_license_info = st.session_state.current_licenses.get(service_name, None)
            
            # Initialize service data if not exists
            if service_key not in st.session_state.operational_services["IT"]:
                st.session_state.operational_services["IT"][service_key] = {
                    'selected': False,
                    'requested_count': current_license_info['current_count'] if current_license_info else 0,
                    'new_implementation': not bool(current_license_info),
                    'annual_cost': 0
                }
            
            service_data = st.session_state.operational_services["IT"][service_key]
            is_currently_selected = service_data.get('selected', False)
            
            # Only show if selected or if user wants to see all
            if is_currently_selected or show_all:
                # Service card with enhanced editing
                status_color = SHARED_SERVICE_DEPARTMENTS["IT"]["color"] if is_currently_selected else "#9ca3af"
                status_text = "✅ SELECTED" if is_currently_selected else "Available"
                
                st.markdown(f"""
                <div class='service-card' style='border-color: {status_color}; position: relative;'>
                    <div style='position: absolute; top: 10px; right: 10px; background: {status_color}; color: white; padding: 0.25rem 0.5rem; border-radius: 8px; font-size: 0.7rem; font-weight: 600;'>{status_text}</div>
                    <h4>{service_name}</h4>
                    <p style='color: #6b7280; font-size: 0.9em;'>{details['description']}</p>
                    <div style='background: {SHARED_SERVICE_DEPARTMENTS["IT"]["color"]}10; padding: 0.5rem; border-radius: 8px; margin: 0.5rem 0;'>
                        💰 SAR {details['price_per_user']}/user/month<br>
                        🆕 Setup Cost: SAR {details['setup_cost']:,}
                        {f"<br>📊 Current: {current_license_info['current_count']} licenses" if current_license_info else ""}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Enhanced selection controls
                selected = st.checkbox(f"Include {service_name}", 
                                     key=f"IT_{service_key}_selected",
                                     value=service_data['selected'])
                
                if selected:
                    if current_license_info:
                        # Existing service - show license delta management
                        st.markdown(f"**Current Licenses:** {current_license_info['current_count']}")
                        
                        min_allowed = current_license_info['min_commitment'] if not current_license_info['can_reduce'] else 0
                        
                        requested_count = st.number_input(
                            f"Requested License Count", 
                            min_value=min_allowed,
                            value=max(service_data['requested_count'], min_allowed),
                            key=f"IT_{service_key}_count",
                            help=f"Minimum allowed: {min_allowed} licenses"
                        )
                        
                        # Calculate delta with visual indicator
                        license_delta = requested_count - current_license_info['current_count']
                        
                        if license_delta > 0:
                            st.success(f"➕ Adding {license_delta} new licenses")
                            monthly_cost = details['price_per_user'] * license_delta
                            annual_cost = monthly_cost * 12
                            setup_cost = 0  # No setup for additional licenses
                            new_implementation = False
                        elif license_delta < 0:
                            if current_license_info['can_reduce']:
                                st.warning(f"➖ Reducing {abs(license_delta)} licenses")
                                annual_cost = 0  # No additional cost for reductions
                                setup_cost = 0
                            else:
                                st.error(f"❌ Cannot reduce licenses below {current_license_info['min_commitment']} (contract restriction)")
                                annual_cost = 0
                                setup_cost = 0
                            monthly_cost = 0
                            new_implementation = False
                        else:
                            st.info("📊 No change in license count")
                            annual_cost = 0
                            setup_cost = 0
                            monthly_cost = 0
                            new_implementation = False
                        
                    else:
                        # New service
                        new_implementation = st.checkbox("🆕 New Implementation", 
                                                       key=f"IT_{service_key}_new_impl",
                                                       value=service_data.get('new_implementation', True))
                        
                        requested_count = st.number_input(f"Number of Licenses", 
                                                        min_value=0, 
                                                        value=service_data['requested_count'],
                                                        key=f"IT_{service_key}_count")
                        
                        if requested_count > 0:
                            monthly_cost = details['price_per_user'] * requested_count
                            annual_cost = monthly_cost * 12
                            setup_cost = details['setup_cost'] if new_implementation else 0
                    
                    # Update session state
                    total_cost = annual_cost + setup_cost
                    st.session_state.operational_services["IT"][service_key] = {
                        'selected': True,
                        'requested_count': requested_count,
                        'new_implementation': new_implementation if not current_license_info else False,
                        'annual_cost': total_cost,
                        'current_count': current_license_info['current_count'] if current_license_info else 0,
                        'license_delta': license_delta if current_license_info else requested_count
                    }
                    
                    # Enhanced cost display
                    if total_cost > 0:
                        st.markdown(f"""
                        <div class='cost-display' style='border-color: {SHARED_SERVICE_DEPARTMENTS["IT"]["color"]}; background: {SHARED_SERVICE_DEPARTMENTS["IT"]["color"]}10;'>
                            📊 Monthly: SAR {monthly_cost:,.0f}<br>
                            🏗️ Setup: SAR {setup_cost:,.0f}<br>
                            <strong>Annual Total: SAR {total_cost:,.0f}</strong>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Save changes indicator
                        if is_currently_selected and total_cost != service_data.get('annual_cost', 0):
                            st.info("💾 Changes will be saved automatically")
                else:
                    # If deselected, clear the data
                    st.session_state.operational_services["IT"][service_key] = {
                        'selected': False,
                        'requested_count': 0,
                        'new_implementation': False,
                        'annual_cost': 0
                    }

def show_general_services_with_editing(department):
    """Show services for non-IT departments with editing capabilities"""
    st.markdown(f"### {SHARED_SERVICE_DEPARTMENTS[department]['icon']} {SHARED_SERVICE_DEPARTMENTS[department]['title']} Services - Add or Modify")
    
    services = st.session_state.admin_services[department]
    
    # Add expand/collapse for better UX
    show_all = st.checkbox("🔍 Show all available services", value=False)
    
    col1, col2 = st.columns(2)
    service_items = list(services.items())
    
    for i, (service_name, details) in enumerate(service_items):
        col = col1 if i % 2 == 0 else col2
        
        with col:
            service_key = service_name.replace(' ', '_').lower()
            
            # Initialize service data if not exists
            if service_key not in st.session_state.operational_services[department]:
                st.session_state.operational_services[department][service_key] = {
                    'selected': False,
                    'volume': 0,
                    'new_implementation': False,
                    'annual_cost': 0
                }
            
            service_data = st.session_state.operational_services[department][service_key]
            is_currently_selected = service_data.get('selected', False)
            
            # Only show if selected or if user wants to see all
            if is_currently_selected or show_all:
                # Determine pricing model
                pricing_key = next((k for k in details.keys() if k.startswith('price_per_')), 'price_per_user')
                unit_name = pricing_key.replace('price_per_', '').replace('_', ' ').title()
                unit_price = details[pricing_key]
                
                # Enhanced service card
                status_color = SHARED_SERVICE_DEPARTMENTS[department]["color"] if is_currently_selected else "#9ca3af"
                status_text = "✅ SELECTED" if is_currently_selected else "Available"
                
                st.markdown(f"""
                <div class='service-card' style='border-color: {status_color}; position: relative;'>
                    <div style='position: absolute; top: 10px; right: 10px; background: {status_color}; color: white; padding: 0.25rem 0.5rem; border-radius: 8px; font-size: 0.7rem; font-weight: 600;'>{status_text}</div>
                    <h4>{service_name}</h4>
                    <p style='color: #6b7280; font-size: 0.9em;'>{details['description']}</p>
                    <div style='background: {SHARED_SERVICE_DEPARTMENTS[department]["color"]}10; padding: 0.5rem; border-radius: 8px; margin: 0.5rem 0;'>
                        💰 SAR {unit_price}/{unit_name.lower()}/month<br>
                        🆕 Setup Cost: SAR {details['setup_cost']:,}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Enhanced service selection controls
                selected = st.checkbox(f"Include {service_name}", 
                                     key=f"{department}_{service_key}_selected",
                                     value=service_data['selected'])
                
                if selected:
                    new_impl = st.checkbox("New Implementation", 
                                         key=f"{department}_{service_key}_new_impl",
                                         value=service_data['new_implementation'])
                    
                    volume = st.number_input(f"Number of {unit_name}s", 
                                           min_value=0, 
                                           value=service_data['volume'],
                                           key=f"{department}_{service_key}_volume")
                    
                    if volume > 0:
                        if 'per_user' in pricing_key:
                            monthly_cost = unit_price * volume
                            annual_cost = monthly_cost * 12
                        else:
                            annual_cost = unit_price * volume
                            monthly_cost = annual_cost / 12
                        
                        setup_cost = details['setup_cost'] if new_impl else 0
                        total_cost = annual_cost + setup_cost
                        
                        st.markdown(f"""
                        <div class='cost-display' style='border-color: {SHARED_SERVICE_DEPARTMENTS[department]["color"]}; background: {SHARED_SERVICE_DEPARTMENTS[department]["color"]}10;'>
                            📊 Annual: SAR {annual_cost:,.0f}<br>
                            🏗️ Setup: SAR {setup_cost:,.0f}<br>
                            <strong>Total: SAR {total_cost:,.0f}</strong>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Update session state
                        st.session_state.operational_services[department][service_key] = {
                            'selected': True,
                            'volume': volume,
                            'new_implementation': new_impl,
                            'annual_cost': total_cost
                        }
                        
                        # Save changes indicator
                        if is_currently_selected and total_cost != service_data.get('annual_cost', 0):
                            st.info("💾 Changes will be saved automatically")
                    else:
                        st.session_state.operational_services[department][service_key] = {
                            'selected': True,
                            'volume': 0,
                            'new_implementation': new_impl,
                            'annual_cost': 0
                        }
                else:
                    st.session_state.operational_services[department][service_key] = {
                        'selected': False,
                        'volume': 0,
                        'new_implementation': False,
                        'annual_cost': 0
                    }

def show_custom_services_section_with_editing(department):
    """Show custom services section with comprehensive editing capabilities"""
    st.markdown("---")
    st.markdown("### ➕ Custom Services")
    
    dept_config = SHARED_SERVICE_DEPARTMENTS[department]
    
    # Show existing custom services with edit/remove options
    if st.session_state.custom_services[department]:
        st.markdown("#### Your Custom Services")
        
        for i, service in enumerate(st.session_state.custom_services[department]):
            with st.expander(f"✏️ Edit: {service['name']} - SAR {service['annual_cost']:,.0f}"):
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    new_name = st.text_input("Service Name", value=service['name'], key=f"edit_custom_name_{i}")
                    new_description = st.text_area("Description", value=service['description'], key=f"edit_custom_desc_{i}")
                
                with col2:
                    new_price = st.number_input("Annual Cost (SAR)", min_value=0, value=service['annual_cost'], key=f"edit_custom_price_{i}")
                    new_setup = st.number_input("Setup Cost (SAR)", min_value=0, value=service.get('setup_cost', 0), key=f"edit_custom_setup_{i}")
                
                with col3:
                    if st.button("💾 Update", key=f"update_custom_{i}", use_container_width=True):
                        st.session_state.custom_services[department][i] = {
                            'name': new_name,
                            'description': new_description,
                            'annual_cost': new_price,
                            'setup_cost': new_setup
                        }
                        st.success(f"✅ Updated {new_name}")
                        st.rerun()
                    
                    if st.button("🗑️ Remove", key=f"remove_custom_edit_{i}", use_container_width=True):
                        service_name = service['name']
                        st.session_state.custom_services[department].pop(i)
                        st.success(f"🗑️ Removed {service_name}")
                        st.rerun()
    
    # Add new custom service
    with st.expander("➕ Add New Custom Service"):
        with st.form(f"custom_service_{department}"):
            col1, col2 = st.columns(2)
            
            with col1:
                custom_name = st.text_input("Service Name")
                custom_description = st.text_area("Description")
            
            with col2:
                custom_price = st.number_input("Annual Cost (SAR)", min_value=0, value=50000)
                custom_setup = st.number_input("Setup Cost (SAR)", min_value=0, value=0)
            
            if st.form_submit_button("Add Custom Service", type="primary"):
                if custom_name and custom_description:
                    custom_service = {
                        'name': custom_name,
                        'description': custom_description,
                        'annual_cost': custom_price,
                        'setup_cost': custom_setup
                    }
                    st.session_state.custom_services[department].append(custom_service)
                    st.success(f"✅ Added custom service: {custom_name}")
                    st.rerun()
                else:
                    st.error("Please provide both service name and description.")

def show_support_step():
    """Step 6: Enhanced Support Package Selection with Editing"""
    if not st.session_state.selected_department:
        navigate_to_step('department_selection')
        return
    
    dept = st.session_state.selected_department
    dept_config = SHARED_SERVICE_DEPARTMENTS[dept]
    
    st.markdown(f"## 🛠️ {dept_config['title']} - Support Packages")
    
    # Check if user has existing selections
    current_package = st.session_state.support_packages[dept]
    current_extras = st.session_state.support_extras[dept]
    has_existing_support = current_package is not None
    
    if has_existing_support:
        st.markdown(f"""
        <div class='success-message'>
            ✅ Current Selection: <strong>{current_package}</strong> - You can modify your support package selection below.
        </div>
        """, unsafe_allow_html=True)
        
        # Show current support summary with remove option
        show_current_support_summary(dept)
    else:
        st.markdown("Choose the support level that best fits your needs.")
    
    # Support package comparison
    packages = st.session_state.admin_support_packages
    
    # Filter packages available for this department
    available_packages = {name: details for name, details in packages.items() 
                         if dept in details.get('departments', [])}
    
    if not available_packages:
        st.warning(f"No support packages are currently available for {dept_config['title']}.")
        # Navigation
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back to Services", use_container_width=True):
                navigate_to_step('services')
        with col2:
            if st.button("Continue to Projects →", type="primary", use_container_width=True):
                navigate_to_step('projects')
        return
    
    # Create comparison table
    comparison_data = {
        'Package': list(available_packages.keys()),
        'Price (SAR)': [f"SAR {pkg['price']:,.0f}" for pkg in available_packages.values()],
        'Support Requests': [pkg['support_requests'] for pkg in available_packages.values()],
        'Training Sessions': [pkg['training'] for pkg in available_packages.values()],
        'Custom Reports': [pkg['reports'] for pkg in available_packages.values()],
        'Improvement Hours': [pkg['improvement_hours'] for pkg in available_packages.values()],
        'Description': [pkg['description'] for pkg in available_packages.values()]
    }
    
    df = pd.DataFrame(comparison_data)
    st.dataframe(df, use_container_width=True)
    
    # Enhanced package selection with editing
    st.markdown("### Select or Change Your Support Package")
    
    cols = st.columns(len(available_packages))
    
    for i, (package_name, details) in enumerate(available_packages.items()):
        with cols[i]:
            is_selected = st.session_state.support_packages[dept] == package_name
            
            # Enhanced package card with selection status
            if is_selected:
                bg_color = f"{dept_config['color']}20"
                border_color = dept_config['color']
                status_badge = f'<div style="position: absolute; top: 10px; right: 10px; background: {dept_config["color"]}; color: white; padding: 0.25rem 0.5rem; border-radius: 8px; font-size: 0.7rem; font-weight: 600;">SELECTED</div>'
            else:
                bg_color = "#f8fafc"
                border_color = "#e5e7eb"
                status_badge = ""
            
            st.markdown(f"""
            <div style='background: {bg_color}; border: 3px solid {border_color}; border-radius: 12px; padding: 1rem; text-align: center; margin-bottom: 1rem; position: relative; min-height: 200px;'>
                {status_badge}
                <h4 style='margin: 0 0 0.5rem 0;'>{package_name}</h4>
                <h3 style='color: {dept_config["color"]}; margin: 0 0 0.5rem 0;'>SAR {details["price"]:,.0f}</h3>
                <p style='font-size: 0.85em; margin: 0;'>{details["description"]}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            **🛠️ Support:** {details['support_requests']}  
            **🎓 Training:** {details['training']}  
            **📊 Reports:** {details['reports']}  
            **⚡ Improvement:** {details['improvement_hours']}h
            """)
            
            if is_selected:
                if st.button("🗑️ Remove Selection", 
                            key=f"remove_support_{package_name}_{dept}", 
                            use_container_width=True,
                            type="secondary"):
                    st.session_state.support_packages[dept] = None
                    st.session_state.support_extras[dept] = {'support': 0, 'training': 0, 'reports': 0}
                    st.success(f"Removed {package_name} support package")
                    st.rerun()
            else:
                if st.button(f"Select {package_name}", 
                            key=f"select_support_{package_name}_{dept}", 
                            type="primary",
                            use_container_width=True):
                    st.session_state.support_packages[dept] = package_name
                    st.success(f"✅ Selected {package_name} support package")
                    st.rerun()
    
    # Enhanced additional services section
    if st.session_state.support_packages[dept]:
        st.markdown("---")
        st.markdown("### ➕ Additional Support Services")
        st.markdown("Add extra support beyond your selected package:")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### 🛠️ Extra Support Requests")
            current_extra_support = st.session_state.support_extras[dept]['support']
            extra_support = st.number_input("Additional Support Requests", 
                                          min_value=0, 
                                          value=current_extra_support,
                                          key=f"extra_support_{dept}",
                                          help="SAR 1,800 per additional support request")
            
            if extra_support != current_extra_support:
                st.session_state.support_extras[dept]['support'] = extra_support
                if extra_support > current_extra_support:
                    st.success(f"Added {extra_support - current_extra_support} extra support requests")
                elif extra_support < current_extra_support:
                    st.info(f"Removed {current_extra_support - extra_support} extra support requests")
            
            if extra_support > 0:
                st.info(f"💰 Cost: SAR {extra_support * 1800:,}")
        
        with col2:
            st.markdown("#### 🎓 Extra Training Sessions")
            current_extra_training = st.session_state.support_extras[dept]['training']
            extra_training = st.number_input("Additional Training Sessions", 
                                           min_value=0, 
                                           value=current_extra_training,
                                           key=f"extra_training_{dept}",
                                           help="SAR 5,399 per additional training session")
            
            if extra_training != current_extra_training:
                st.session_state.support_extras[dept]['training'] = extra_training
                if extra_training > current_extra_training:
                    st.success(f"Added {extra_training - current_extra_training} extra training sessions")
                elif extra_training < current_extra_training:
                    st.info(f"Removed {current_extra_training - extra_training} extra training sessions")
            
            if extra_training > 0:
                st.info(f"💰 Cost: SAR {extra_training * 5399:,}")
        
        with col3:
            st.markdown("#### 📋 Extra Custom Reports")
            current_extra_reports = st.session_state.support_extras[dept]['reports']
            extra_reports = st.number_input("Additional Custom Reports", 
                                          min_value=0, 
                                          value=current_extra_reports,
                                          key=f"extra_reports_{dept}",
                                          help="SAR 5,399 per additional custom report")
            
            if extra_reports != current_extra_reports:
                st.session_state.support_extras[dept]['reports'] = extra_reports
                if extra_reports > current_extra_reports:
                    st.success(f"Added {extra_reports - current_extra_reports} extra reports")
                elif extra_reports < current_extra_reports:
                    st.info(f"Removed {current_extra_reports - extra_reports} extra reports")
            
            if extra_reports > 0:
                st.info(f"💰 Cost: SAR {extra_reports * 5399:,}")
        
        # Total support cost display with change indicator
        total_support = calculate_support_total(dept)
        st.markdown(f"""
        <div class='cost-display' style='border-color: {dept_config["color"]}; background: {dept_config["color"]}10;'>
            💰 Total Support Package Cost: <strong>SAR {total_support:,.0f}</strong>
        </div>
        """, unsafe_allow_html=True)
    
    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Services", use_container_width=True):
            navigate_to_step('services')
    with col2:
        if st.button("Continue to Projects →", type="primary", use_container_width=True):
            navigate_to_step('projects')

def show_current_support_summary(dept):
    """Show current support package selection with options to modify"""
    st.markdown("### 📋 Current Support Selection")
    
    current_package = st.session_state.support_packages[dept]
    if current_package:
        package_details = st.session_state.admin_support_packages[current_package]
        extras = st.session_state.support_extras[dept]
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"""
            **Selected Package:** {current_package}  
            **Base Cost:** SAR {package_details['price']:,.0f}  
            **Includes:** {package_details['support_requests']} support requests, {package_details['training']} training sessions, {package_details['reports']} reports, {package_details['improvement_hours']}h improvement
            """)
            
            # Show extras if any
            extra_items = []
            if extras['support'] > 0:
                extra_items.append(f"{extras['support']} extra support requests")
            if extras['training'] > 0:
                extra_items.append(f"{extras['training']} extra training sessions")
            if extras['reports'] > 0:
                extra_items.append(f"{extras['reports']} extra reports")
            
            if extra_items:
                st.markdown(f"**Additional Services:** {', '.join(extra_items)}")
        
        with col2:
            total_cost = calculate_support_total(dept)
            st.markdown(f"**Total Cost:**  \nSAR {total_cost:,.0f}")
    
    st.markdown("---")

def show_projects_step():
    """Step 7: Enhanced Implementation Projects with Comprehensive Editing"""
    if not st.session_state.selected_department:
        navigate_to_step('department_selection')
        return
    
    dept = st.session_state.selected_department
    dept_config = SHARED_SERVICE_DEPARTMENTS[dept]
    
    st.markdown(f"## 🚀 {dept_config['title']} - Implementation Projects")
    
    # Check if user has existing projects
    existing_projects = st.session_state.implementation_projects[dept]
    has_existing_projects = len(existing_projects) > 0
    
    if has_existing_projects:
        st.markdown(f"""
        <div class='success-message'>
            ✅ You have {len(existing_projects)} implementation project(s). You can edit, add more, or remove projects below.
        </div>
        """, unsafe_allow_html=True)
        
        # Show current projects with edit/remove options
        show_current_projects_summary(dept)
    else:
        st.markdown("Define custom implementation projects and initiatives.")
    
    # Enhanced project addition form
    with st.expander("➕ Add New Implementation Project", expanded=not has_existing_projects):
        with st.form(f"new_project_{dept}"):
            col1, col2 = st.columns(2)
            
            with col1:
                project_name = st.text_input("Project Name", placeholder="Enter project name")
                project_description = st.text_area("Project Description", placeholder="Detailed project description")
                
                # Category selection based on department
                categories = st.session_state.admin_project_categories[dept]
                selected_category = st.selectbox("Project Category", options=list(categories.keys()))
                project_type = st.selectbox("Specific Project Type", options=categories[selected_category])
                
                timeline = st.selectbox("Timeline", ["Q1 2025", "Q2 2025", "Q3 2025", "Q4 2025", "Multi-quarter"])
            
            with col2:
                budget = st.number_input("Budget (SAR)", min_value=0, value=100000, step=10000)
                priority = st.select_slider("Priority", ["Low", "Medium", "High", "Critical"], value="Medium")
                success_criteria = st.text_area("Success Criteria", placeholder="Define success metrics")
                
                # Special RPA handling for IT department
                if dept == "IT" and "RPA" in project_type:
                    st.markdown("#### 🤖 RPA Package Selection")
                    use_rpa_package = st.checkbox("Use Predefined RPA Package")
                    
                    if use_rpa_package:
                        rpa_package = st.selectbox("RPA Package", list(st.session_state.admin_rpa_packages.keys()))
                        if rpa_package:
                            package_details = st.session_state.admin_rpa_packages[rpa_package]
                            st.info(f"Year 1: SAR {package_details['year_1_total']:,} | {package_details['processes_covered']}")
                            budget = package_details['year_1_total']
            
            col_submit1, col_submit2 = st.columns(2)
            with col_submit1:
                if st.form_submit_button("Add Project", type="primary", use_container_width=True):
                    if project_name and project_description and budget > 0:
                        project = {
                            'name': project_name,
                            'description': project_description,
                            'category': selected_category,
                            'type': project_type,
                            'timeline': timeline,
                            'budget': budget,
                            'priority': priority,
                            'success_criteria': success_criteria,
                            'created_date': datetime.now().strftime("%Y-%m-%d"),
                            'id': str(uuid.uuid4())[:8]  # Add unique ID for editing
                        }
                        
                        # Add RPA details if applicable
                        if dept == "IT" and "RPA" in project_type and locals().get('use_rpa_package', False):
                            project['rpa_package'] = rpa_package
                            project['rpa_details'] = st.session_state.admin_rpa_packages[rpa_package]
                        
                        st.session_state.implementation_projects[dept].append(project)
                        st.success(f"✅ Added project: {project_name}")
                        st.rerun()
                    else:
                        st.error("Please fill in all required fields.")
            
            with col_submit2:
                if st.form_submit_button("Clear Form", use_container_width=True):
                    st.rerun()
    
    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Support", use_container_width=True):
            navigate_to_step('support')
    with col2:
        # Check if high-value service terms are needed
        total_budget = calculate_operational_total(dept) + calculate_support_total(dept) + calculate_project_total(dept)
        if total_budget > 100000:
            if st.button("Continue to High-Value Terms →", type="primary", use_container_width=True):
                navigate_to_step('terms_submission')
        else:
            if st.button("Continue to Final Terms →", type="primary", use_container_width=True):
                navigate_to_step('terms_submission')

def show_current_projects_summary(dept):
    """Show current implementation projects with comprehensive editing options"""
    st.markdown(f"### 📋 Your {SHARED_SERVICE_DEPARTMENTS[dept]['title']} Implementation Projects")
    
    existing_projects = st.session_state.implementation_projects[dept]
    total_budget = sum(project['budget'] for project in existing_projects)
    
    # Project summary header
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Projects", len(existing_projects))
    with col2:
        st.metric("Total Budget", f"SAR {total_budget:,.0f}")
    with col3:
        avg_budget = total_budget / len(existing_projects) if existing_projects else 0
        st.metric("Average Budget", f"SAR {avg_budget:,.0f}")
    
    # Individual project cards with edit options
    for i, project in enumerate(existing_projects):
        priority_colors = {
            'Low': '#10b981',
            'Medium': '#f59e0b',
            'High': '#ef4444',
            'Critical': '#dc2626'
        }
        
        priority_color = priority_colors.get(project['priority'], '#6b7280')
        
        with st.expander(f"✏️ Edit: {project['name']} - SAR {project['budget']:,.0f} ({project['priority']} Priority)"):
            # Edit form for this project
            with st.form(f"edit_project_{i}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    new_name = st.text_input("Project Name", value=project['name'], key=f"edit_name_{i}")
                    new_description = st.text_area("Description", value=project['description'], key=f"edit_desc_{i}")
                    new_timeline = st.selectbox("Timeline", 
                                               ["Q1 2025", "Q2 2025", "Q3 2025", "Q4 2025", "Multi-quarter"],
                                               index=["Q1 2025", "Q2 2025", "Q3 2025", "Q4 2025", "Multi-quarter"].index(project['timeline']),
                                               key=f"edit_timeline_{i}")
                
                with col2:
                    new_budget = st.number_input("Budget (SAR)", 
                                               min_value=0, 
                                               value=project['budget'],
                                               step=10000,
                                               key=f"edit_budget_{i}")
                    new_priority = st.select_slider("Priority", 
                                                   ["Low", "Medium", "High", "Critical"],
                                                   value=project['priority'],
                                                   key=f"edit_priority_{i}")
                    new_success_criteria = st.text_area("Success Criteria", 
                                                       value=project.get('success_criteria', ''),
                                                       key=f"edit_success_{i}")
                
                # Form buttons
                col_update, col_remove, col_duplicate = st.columns(3)
                
                with col_update:
                    if st.form_submit_button("💾 Update Project", type="primary", use_container_width=True):
                        # Update the project
                        st.session_state.implementation_projects[dept][i].update({
                            'name': new_name,
                            'description': new_description,
                            'timeline': new_timeline,
                            'budget': new_budget,
                            'priority': new_priority,
                            'success_criteria': new_success_criteria,
                            'last_modified': datetime.now().strftime("%Y-%m-%d %H:%M")
                        })
                        st.success(f"✅ Updated project: {new_name}")
                        st.rerun()
                
                with col_remove:
                    if st.form_submit_button("🗑️ Remove Project", use_container_width=True):
                        project_name = project['name']
                        st.session_state.implementation_projects[dept].pop(i)
                        st.success(f"🗑️ Removed project: {project_name}")
                        st.rerun()
                
                with col_duplicate:
                    if st.form_submit_button("📋 Duplicate", use_container_width=True):
                        # Create a duplicate with modified name
                        duplicate_project = project.copy()
                        duplicate_project['name'] = f"{project['name']} (Copy)"
                        duplicate_project['id'] = str(uuid.uuid4())[:8]
                        duplicate_project['created_date'] = datetime.now().strftime("%Y-%m-%d")
                        
                        st.session_state.implementation_projects[dept].append(duplicate_project)
                        st.success(f"📋 Duplicated project: {duplicate_project['name']}")
                        st.rerun()
            
            # Project details display (read-only info)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"**Category:** {project.get('category', 'General')}")
                st.markdown(f"**Type:** {project.get('type', 'General')}")
            with col2:
                st.markdown(f"**Created:** {project.get('created_date', 'Unknown')}")
                if 'last_modified' in project:
                    st.markdown(f"**Modified:** {project['last_modified']}")
            with col3:
                if project.get('rpa_package'):
                    st.markdown(f"**RPA Package:** {project['rpa_package']}")
                st.markdown(f"**Project ID:** {project.get('id', 'N/A')}")
    
    # Bulk actions
    if len(existing_projects) > 1:
        st.markdown("---")
        st.markdown("### 🔧 Bulk Actions")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📊 Sort by Budget", use_container_width=True):
                st.session_state.implementation_projects[dept].sort(key=lambda x: x['budget'], reverse=True)
                st.success("Projects sorted by budget (highest first)")
                st.rerun()
        
        with col2:
            if st.button("⚡ Sort by Priority", use_container_width=True):
                priority_order = {'Critical': 4, 'High': 3, 'Medium': 2, 'Low': 1}
                st.session_state.implementation_projects[dept].sort(key=lambda x: priority_order.get(x['priority'], 0), reverse=True)
                st.success("Projects sorted by priority")
                st.rerun()
        
        with col3:
            if st.button("📅 Sort by Timeline", use_container_width=True):
                timeline_order = {'Q1 2025': 1, 'Q2 2025': 2, 'Q3 2025': 3, 'Q4 2025': 4, 'Multi-quarter': 5}
                st.session_state.implementation_projects[dept].sort(key=lambda x: timeline_order.get(x['timeline'], 6))
                st.success("Projects sorted by timeline")
                st.rerun()
        
        with col4:
            if st.button("🗑️ Clear All Projects", use_container_width=True, type="secondary"):
                if st.session_state.get(f'confirm_clear_{dept}', False):
                    st.session_state.implementation_projects[dept] = []
                    st.session_state[f'confirm_clear_{dept}'] = False
                    st.success("All projects cleared")
                    st.rerun()
                else:
                    st.session_state[f'confirm_clear_{dept}'] = True
                    st.warning("Click again to confirm clearing all projects")
    
    st.markdown("---")

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
