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

# ==================== CONFIGURATION DATA ====================

# Admin Credentials
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

# Shared Service Departments Configuration
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

# Default Service Data
DEFAULT_SERVICES = {
    "IT": {
        "Microsoft 365 E3": {"price_per_user": 82, "setup_cost": 5000, "description": "Premium productivity suite with advanced security and compliance"},
        "Oracle ERP Cloud": {"price_per_user": 180, "setup_cost": 25000, "description": "Complete enterprise resource planning solution"},
        "Power BI Premium": {"price_per_user": 75, "setup_cost": 4000, "description": "Advanced business intelligence platform"},
        "Microsoft Teams Phone": {"price_per_user": 28, "setup_cost": 3000, "description": "Cloud-based phone system integrated with Teams"}
    },
    "HR": {
        "Talent Acquisition Platform": {"price_per_user": 120, "setup_cost": 15000, "description": "End-to-end recruitment and hiring platform"},
        "Learning Management System": {"price_per_user": 45, "setup_cost": 8000, "description": "Employee training and development platform"},
        "Performance Management": {"price_per_user": 65, "setup_cost": 12000, "description": "Goal setting and performance review system"},
        "HR Analytics Dashboard": {"price_per_user": 85, "setup_cost": 10000, "description": "Workforce analytics and reporting platform"}
    },
    "Legal": {
        "Contract Management System": {"price_per_contract": 250, "setup_cost": 20000, "description": "Lifecycle contract management and compliance"},
        "Legal Research Platform": {"price_per_user": 150, "setup_cost": 5000, "description": "Comprehensive legal research and documentation"},
        "Compliance Management": {"price_per_regulation": 500, "setup_cost": 15000, "description": "Regulatory compliance tracking and reporting"},
        "IP Management System": {"price_per_asset": 100, "setup_cost": 12000, "description": "Intellectual property portfolio management"}
    },
    "Procurement": {
        "E-Procurement Platform": {"price_per_transaction": 25, "setup_cost": 18000, "description": "Digital procurement and supplier management"},
        "Supplier Portal": {"price_per_supplier": 120, "setup_cost": 8000, "description": "Supplier onboarding and management portal"},
        "Contract Management": {"price_per_contract": 150, "setup_cost": 12000, "description": "Procurement contract lifecycle management"},
        "Spend Analytics": {"price_per_user": 95, "setup_cost": 10000, "description": "Procurement spend analysis and reporting"}
    },
    "Facility_Safety": {
        "Facility Management System": {"price_per_sq_meter": 12, "setup_cost": 25000, "description": "Comprehensive facility operations management"},
        "Safety Management Platform": {"price_per_employee": 45, "setup_cost": 18000, "description": "Workplace safety tracking and compliance"},
        "Security Access Control": {"price_per_access_point": 180, "setup_cost": 35000, "description": "Physical security and access management"},
        "Environmental Monitoring": {"price_per_monitoring_point": 250, "setup_cost": 15000, "description": "Environmental compliance and monitoring"}
    }
}

# Support Packages
DEFAULT_SUPPORT_PACKAGES = {
    "Basic": {"price": 52000, "support_requests": 50, "training": 0, "reports": 0, "description": "Essential support for small teams"},
    "Bronze": {"price": 195975, "support_requests": 100, "training": 2, "reports": 2, "description": "Enhanced support for growing organizations"},
    "Silver": {"price": 649498, "support_requests": 400, "training": 5, "reports": 5, "description": "Comprehensive support for medium enterprises"},
    "Gold": {"price": 1578139, "support_requests": 1000, "training": 10, "reports": 10, "description": "Premium support for large organizations"},
    "Platinum": {"price": 2500000, "support_requests": 1575, "training": 20, "reports": 15, "description": "Enterprise-grade support with dedicated resources"}
}

# Terms & Conditions Templates
TERMS_TEMPLATES = {
    "system_wide": {
        "title": "System-Wide Terms & Conditions",
        "content": """
        ## General Usage Terms
        By accessing and using the Alkhorayef Group Shared Services Budgeting System, you agree to comply with these terms and conditions.

        ## Data Privacy & Security
        All data entered into the system is protected under our comprehensive data protection policies in compliance with applicable regulations.

        ## Service Framework
        This system facilitates the selection and budgeting of shared services across Alkhorayef Group companies.

        ## User Responsibilities
        Users are responsible for accurate data entry and compliance with company policies when submitting budget requests.

        ## Limitation of Liability
        The shared services departments provide services in good faith and limit liability as outlined in individual service agreements.
        """
    },
    "IT": {
        "title": "IT Shared Services Terms",
        "content": """
        ## Software Licensing Obligations
        Users must comply with all software license terms and usage restrictions.

        ## Data Security Requirements
        IT services include security protocols that must be followed by all users.

        ## System Integration Responsibilities
        Companies requesting IT services must provide necessary access and cooperation for implementations.

        ## Support Procedures
        Support requests must follow established procedures and service level agreements.
        """
    },
    "HR": {
        "title": "HR Shared Services Terms",
        "content": """
        ## Employee Data Privacy
        All HR services comply with employment law and data privacy regulations.

        ## Training Obligations
        Companies must ensure employee participation in required training programs.

        ## Performance Management Participation
        HR services require active participation in performance management processes.

        ## Employment Policy Compliance
        All HR services must align with company employment policies and procedures.
        """
    },
    "Legal": {
        "title": "Legal Shared Services Terms",
        "content": """
        ## Attorney-Client Privilege
        Legal services maintain attorney-client privilege where applicable.

        ## Conflict Disclosure
        Companies must disclose any potential conflicts of interest.

        ## Legal Advice Limitations
        Legal services are provided within the scope of shared services agreements.

        ## Document Retention
        Legal documents must be retained according to regulatory requirements.
        """
    },
    "Procurement": {
        "title": "Procurement Shared Services Terms",
        "content": """
        ## Purchase Commitments
        Companies must honor purchase commitments made through the procurement system.

        ## Supplier Compliance
        All suppliers must meet Alkhorayef Group compliance requirements.

        ## Contract Procedures
        Procurement contracts must follow established procedures and approval workflows.

        ## Payment Terms
        Payment obligations must be met according to agreed terms and conditions.
        """
    },
    "Facility_Safety": {
        "title": "Facilities & Safety Shared Services Terms",
        "content": """
        ## Safety Compliance
        All facility users must comply with safety protocols and procedures.

        ## Facility Access Rules
        Access to facilities is governed by security and safety protocols.

        ## Emergency Procedures
        Users must be familiar with and follow emergency response procedures.

        ## Environmental Compliance
        All activities must comply with environmental regulations and policies.
        """
    }
}

# ==================== CSS STYLING ====================

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
    
    .terms-card {
        background: #fef7ff;
        border: 2px solid #8b5cf6;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 6px solid #8b5cf6;
    }
    
    .cost-display {
        background: #f0f9ff;
        border: 2px solid #0ea5e9;
        border-radius: 12px;
        padding: 1rem;
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
    
    .step-indicator {
        display: flex;
        justify-content: space-between;
        margin: 2rem 0;
        padding: 0 1rem;
    }
    
    .step {
        display: flex;
        flex-direction: column;
        align-items: center;
        flex: 1;
        position: relative;
    }
    
    .step-circle {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        color: white;
        margin-bottom: 0.5rem;
    }
    
    .step-circle.completed {
        background: #10b981;
    }
    
    .step-circle.current {
        background: #3b82f6;
        box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.2);
    }
    
    .step-circle.pending {
        background: #9ca3af;
    }
    
    .admin-section {
        background: #fef2f2;
        border: 2px solid #fecaca;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 6px solid #dc2626;
    }
    
    .success-message {
        background: #f0fdf4;
        border: 2px solid #10b981;
        color: #065f46;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .warning-message {
        background: #fffbeb;
        border: 2px solid #f59e0b;
        color: #92400e;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
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
    
    # Terms & Conditions tracking
    if 'terms_accepted' not in st.session_state:
        st.session_state.terms_accepted = {
            'system_wide': False,
            'department_specific': {},
            'service_specific': {},
            'budget_submission': False
        }
    
    # Service selections by department
    if 'operational_services' not in st.session_state:
        st.session_state.operational_services = {dept: {} for dept in SHARED_SERVICE_DEPARTMENTS.keys()}
    if 'custom_services' not in st.session_state:
        st.session_state.custom_services = {dept: [] for dept in SHARED_SERVICE_DEPARTMENTS.keys()}
    if 'support_packages' not in st.session_state:
        st.session_state.support_packages = {dept: None for dept in SHARED_SERVICE_DEPARTMENTS.keys()}
    if 'implementation_projects' not in st.session_state:
        st.session_state.implementation_projects = {dept: [] for dept in SHARED_SERVICE_DEPARTMENTS.keys()}
    
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
    """Define the workflow steps"""
    return [
        {'key': 'company_info', 'title': 'Company Info', 'icon': '🏢'},
        {'key': 'terms_system', 'title': 'System Terms', 'icon': '📋'},
        {'key': 'department_selection', 'title': 'Department', 'icon': '🎯'},
        {'key': 'terms_department', 'title': 'Dept Terms', 'icon': '⚖️'},
        {'key': 'services', 'title': 'Services', 'icon': '🛍️'},
        {'key': 'support', 'title': 'Support', 'icon': '🛠️'},
        {'key': 'projects', 'title': 'Projects', 'icon': '🚀'},
        {'key': 'summary', 'title': 'Summary', 'icon': '📊'}
    ]

def show_progress_indicator():
    """Show workflow progress indicator"""
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
            <small style="text-align: center; color: #6b7280;">{step['title']}</small>
        </div>
        '''
    
    step_html += '</div>'
    
    # Progress bar
    progress = (current_index / (len(steps) - 1)) * 100
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

# ==================== TERMS & CONDITIONS ====================

def show_terms_modal(terms_type, department=None):
    """Show terms and conditions modal"""
    if terms_type == 'system_wide':
        terms_data = st.session_state.admin_terms['system_wide']
    elif terms_type == 'department' and department:
        terms_data = st.session_state.admin_terms.get(department, {
            'title': f'{SHARED_SERVICE_DEPARTMENTS[department]["title"]} Terms',
            'content': 'Department-specific terms will be defined here.'
        })
    else:
        return False
    
    st.markdown(f"""
    <div class='terms-card'>
        <h2>{terms_data['title']}</h2>
        <div style='max-height: 400px; overflow-y: auto; padding: 1rem; background: white; border-radius: 8px; margin: 1rem 0;'>
            {terms_data['content'].replace('\n', '<br>')}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col2:
        if st.button("❌ Decline", use_container_width=True):
            st.error("You must accept the terms to continue using the system.")
            return False
    
    with col3:
        if st.button("✅ Accept Terms", use_container_width=True, type="primary"):
            if terms_type == 'system_wide':
                st.session_state.terms_accepted['system_wide'] = True
            elif terms_type == 'department' and department:
                st.session_state.terms_accepted['department_specific'][department] = True
            
            st.success(f"✅ Terms accepted! You can now proceed.")
            return True
    
    return False

# ==================== HEADER COMPONENTS ====================

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
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class='main-header'>
            <h1>💼 Alkhorayef Group</h1>
            <h2>2025 Multi-Department Shared Services Catalogue</h2>
            <p><strong>Budget Year:</strong> 2025 | <strong>Version:</strong> 3.0 | <strong>Environment:</strong> Demo System</p>
        </div>
        """, unsafe_allow_html=True)

def show_sidebar():
    """Show sidebar with navigation and summary"""
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
    
    st.markdown("---")
    
    # Budget summary
    if st.session_state.selected_department:
        show_budget_summary()
    
    # Quick navigation
    st.markdown("### 🧭 Quick Navigation")
    steps = get_workflow_steps()
    
    for step in steps:
        if st.button(f"{step['icon']} {step['title']}", key=f"nav_{step['key']}", use_container_width=True):
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
    else:
        st.markdown("**🔐 Admin Access Required**")
        st.info("Please log in with Department Head credentials")

def show_budget_summary():
    """Show budget summary in sidebar"""
    st.markdown("### 💰 Budget Summary")
    
    total_budget = calculate_total_budget()
    operational_total = calculate_operational_total()
    support_total = calculate_support_total()
    project_total = calculate_project_total()
    
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
                title="Budget Distribution"
            )
            fig.update_layout(height=200, margin=dict(t=30, b=0, l=0, r=0))
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No services selected yet")

# ==================== CALCULATION FUNCTIONS ====================

def calculate_operational_total():
    """Calculate total operational services cost"""
    if not st.session_state.selected_department:
        return 0
    
    total = 0
    dept = st.session_state.selected_department
    
    # Predefined services
    for service_name, data in st.session_state.operational_services[dept].items():
        if data.get('selected', False):
            total += data.get('annual_cost', 0)
    
    # Custom services
    for service in st.session_state.custom_services[dept]:
        total += service.get('annual_cost', 0)
    
    return total

def calculate_support_total():
    """Calculate support package cost"""
    if not st.session_state.selected_department:
        return 0
    
    dept = st.session_state.selected_department
    package = st.session_state.support_packages[dept]
    
    if package:
        return st.session_state.admin_support_packages[package]['price']
    
    return 0

def calculate_project_total():
    """Calculate implementation projects cost"""
    if not st.session_state.selected_department:
        return 0
    
    dept = st.session_state.selected_department
    return sum(project.get('budget', 0) for project in st.session_state.implementation_projects[dept])

def calculate_total_budget():
    """Calculate total budget across all areas"""
    return calculate_operational_total() + calculate_support_total() + calculate_project_total()

# ==================== STEP IMPLEMENTATIONS ====================

def show_company_info_step():
    """Step 1: Company Information Collection"""
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
        
        submitted = st.form_submit_button("Continue to Terms & Conditions", type="primary", use_container_width=True)
        
        if submitted:
            if company and department and contact_person and email:
                st.session_state.company_info = {
                    'company': company,
                    'department': department,
                    'contact_person': contact_person,
                    'email': email,
                    'date': datetime.now().strftime("%Y-%m-%d")
                }
                navigate_to_step('terms_system')
            else:
                st.error("Please fill in all required fields.")

def show_system_terms_step():
    """Step 2: System-wide Terms & Conditions"""
    st.markdown("## 📋 System Terms & Conditions")
    st.markdown("Before proceeding, please review and accept our system-wide terms and conditions.")
    
    if not st.session_state.terms_accepted['system_wide']:
        accepted = show_terms_modal('system_wide')
        if accepted:
            navigate_to_step('department_selection')
    else:
        st.markdown("""
        <div class='success-message'>
            ✅ System terms have been accepted. You can proceed to department selection.
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Continue to Department Selection", type="primary", use_container_width=True):
            navigate_to_step('department_selection')

def show_department_selection_step():
    """Step 3: Shared Service Department Selection"""
    st.markdown("## 🎯 Select Shared Service Department")
    st.markdown("Choose the shared service department for which you want to create a budget.")
    
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
            dept_budget = 0
            if has_selections:
                # This would need to be calculated per department
                pass
            
            st.markdown(f"""
            <div class='department-card {"selected" if st.session_state.selected_department == dept_key else ""}' 
                 style='border-color: {dept_config["color"]}; min-height: 200px;'>
                <h1 style='margin: 0; color: {dept_config["color"]}; font-size: 3em;'>{dept_config["icon"]}</h1>
                <h3 style='margin: 0.5rem 0; color: #1f2937;'>{dept_config["title"]}</h3>
                <p style='margin: 0; color: #6b7280; font-size: 0.9em; line-height: 1.4;'>{dept_config["description"]}</p>
                {f'<div style="margin-top: 1rem; padding: 0.5rem; background: {dept_config["color"]}20; border-radius: 8px; color: {dept_config["color"]}; font-weight: 600;">✓ Has Selections</div>' if has_selections else ''}
            </div>
            """, unsafe_allow_html=True)
            
            button_text = f"Continue with {dept_config['title']}" if has_selections else f"Select {dept_config['title']}"
            
            if st.button(button_text, key=f"select_{dept_key}", use_container_width=True, type="primary"):
                st.session_state.selected_department = dept_key
                # Check if department-specific terms are accepted
                if not st.session_state.terms_accepted['department_specific'].get(dept_key, False):
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
    
    if not st.session_state.terms_accepted['department_specific'].get(st.session_state.selected_department, False):
        accepted = show_terms_modal('department', st.session_state.selected_department)
        if accepted:
            navigate_to_step('services')
    else:
        st.markdown(f"""
        <div class='success-message'>
            ✅ {dept_config['title']} terms have been accepted. You can proceed to service selection.
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Continue to Service Selection", type="primary", use_container_width=True):
            navigate_to_step('services')

def show_services_step():
    """Step 5: Operational Services Selection"""
    if not st.session_state.selected_department:
        navigate_to_step('department_selection')
        return
    
    dept = st.session_state.selected_department
    dept_config = SHARED_SERVICE_DEPARTMENTS[dept]
    services = st.session_state.admin_services[dept]
    
    st.markdown(f"## 🛍️ {dept_config['title']} - Operational Services")
    st.markdown(f"Select the operational services you need for {dept_config['title']}.")
    
    # Service selection
    col1, col2 = st.columns(2)
    service_items = list(services.items())
    
    for i, (service_name, details) in enumerate(service_items):
        col = col1 if i % 2 == 0 else col2
        
        with col:
            service_key = service_name.replace(' ', '_').lower()
            
            # Initialize service data if not exists
            if service_key not in st.session_state.operational_services[dept]:
                st.session_state.operational_services[dept][service_key] = {
                    'selected': False,
                    'volume': 0,
                    'new_implementation': False,
                    'annual_cost': 0
                }
            
            service_data = st.session_state.operational_services[dept][service_key]
            
            # Determine pricing model
            pricing_key = next((k for k in details.keys() if k.startswith('price_per_')), 'price_per_user')
            unit_name = pricing_key.replace('price_per_', '').replace('_', ' ').title()
            unit_price = details[pricing_key]
            
            st.markdown(f"""
            <div class='service-card' style='border-color: {dept_config["color"]}40;'>
                <h4>{service_name}</h4>
                <p style='color: #6b7280; font-size: 0.9em;'>{details['description']}</p>
                <div style='background: {dept_config["color"]}10; padding: 0.5rem; border-radius: 8px; margin: 0.5rem 0;'>
                    💰 SAR {unit_price}/{unit_name.lower()}/month<br>
                    🆕 Setup Cost: SAR {details['setup_cost']:,}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Service selection controls
            selected = st.checkbox(f"Include {service_name}", 
                                 key=f"{dept}_{service_key}_selected",
                                 value=service_data['selected'])
            
            if selected:
                new_impl = st.checkbox("New Implementation", 
                                     key=f"{dept}_{service_key}_new_impl",
                                     value=service_data['new_implementation'])
                
                volume = st.number_input(f"Number of {unit_name}s", 
                                       min_value=0, 
                                       value=service_data['volume'],
                                       key=f"{dept}_{service_key}_volume")
                
                if volume > 0:
                    monthly_cost = unit_price * volume
                    annual_cost = monthly_cost * 12
                    setup_cost = details['setup_cost'] if new_impl else 0
                    total_cost = annual_cost + setup_cost
                    
                    st.markdown(f"""
                    <div class='cost-display' style='border-color: {dept_config["color"]}; background: {dept_config["color"]}10;'>
                        📊 Monthly: SAR {monthly_cost:,.0f}<br>
                        🏗️ Setup: SAR {setup_cost:,.0f}<br>
                        <strong>Annual Total: SAR {total_cost:,.0f}</strong>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Update session state
                    st.session_state.operational_services[dept][service_key] = {
                        'selected': True,
                        'volume': volume,
                        'new_implementation': new_impl,
                        'annual_cost': total_cost
                    }
                else:
                    st.session_state.operational_services[dept][service_key] = {
                        'selected': True,
                        'volume': 0,
                        'new_implementation': new_impl,
                        'annual_cost': 0
                    }
            else:
                st.session_state.operational_services[dept][service_key] = {
                    'selected': False,
                    'volume': 0,
                    'new_implementation': False,
                    'annual_cost': 0
                }
    
    # Custom services section
    st.markdown("---")
    st.markdown("### ➕ Add Custom Services")
    
    with st.expander("Add Custom Service"):
        with st.form(f"custom_service_{dept}"):
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
                        'annual_cost': custom_price + custom_setup,
                        'setup_cost': custom_setup
                    }
                    st.session_state.custom_services[dept].append(custom_service)
                    st.success(f"✅ Added custom service: {custom_name}")
                    st.rerun()
    
    # Display custom services
    if st.session_state.custom_services[dept]:
        st.markdown("#### Your Custom Services")
        for i, service in enumerate(st.session_state.custom_services[dept]):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"""
                **{service['name']}** - SAR {service['annual_cost']:,.0f}  
                {service['description']}
                """)
            with col2:
                if st.button("Remove", key=f"remove_custom_{dept}_{i}"):
                    st.session_state.custom_services[dept].pop(i)
                    st.rerun()
    
    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Department Selection", use_container_width=True):
            navigate_to_step('department_selection')
    with col2:
        if st.button("Continue to Support Packages →", type="primary", use_container_width=True):
            navigate_to_step('support')

def show_support_step():
    """Step 6: Support Package Selection"""
    if not st.session_state.selected_department:
        navigate_to_step('department_selection')
        return
    
    dept = st.session_state.selected_department
    dept_config = SHARED_SERVICE_DEPARTMENTS[dept]
    
    st.markdown(f"## 🛠️ {dept_config['title']} - Support Packages")
    st.markdown("Choose the support level that best fits your needs.")
    
    # Support package comparison
    packages = st.session_state.admin_support_packages
    
    # Create comparison table
    comparison_data = {
        'Package': list(packages.keys()),
        'Price (SAR)': [f"SAR {pkg['price']:,.0f}" for pkg in packages.values()],
        'Support Requests': [pkg['support_requests'] for pkg in packages.values()],
        'Training Sessions': [pkg['training'] for pkg in packages.values()],
        'Custom Reports': [pkg['reports'] for pkg in packages.values()],
        'Description': [pkg['description'] for pkg in packages.values()]
    }
    
    df = pd.DataFrame(comparison_data)
    st.dataframe(df, use_container_width=True)
    
    # Package selection
    st.markdown("### Select Your Support Package")
    
    cols = st.columns(len(packages))
    
    for i, (package_name, details) in enumerate(packages.items()):
        with cols[i]:
            is_selected = st.session_state.support_packages[dept] == package_name
            
            # Package card
            bg_color = f"{dept_config['color']}20" if is_selected else "#f8fafc"
            border_color = dept_config['color'] if is_selected else "#e5e7eb"
            
            st.markdown(f"""
            <div style='background: {bg_color}; border: 3px solid {border_color}; border-radius: 12px; padding: 1rem; text-align: center; margin-bottom: 1rem;'>
                <h4 style='margin: 0 0 0.5rem 0;'>{package_name}</h4>
                <h3 style='color: {dept_config["color"]}; margin: 0 0 0.5rem 0;'>SAR {details["price"]:,.0f}</h3>
                <p style='font-size: 0.85em; margin: 0;'>{details["description"]}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            **🛠️ Support Requests:** {details['support_requests']}  
            **🎓 Training Sessions:** {details['training']}  
            **📊 Custom Reports:** {details['reports']}
            """)
            
            button_text = "✅ Selected" if is_selected else f"Select {package_name}"
            button_type = "secondary" if is_selected else "primary"
            
            if st.button(button_text, 
                        key=f"select_support_{package_name}", 
                        disabled=is_selected,
                        type=button_type,
                        use_container_width=True):
                st.session_state.support_packages[dept] = package_name
                st.success(f"✅ Selected {package_name} support package")
                st.rerun()
    
    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Services", use_container_width=True):
            navigate_to_step('services')
    with col2:
        if st.button("Continue to Projects →", type="primary", use_container_width=True):
            navigate_to_step('projects')

def show_projects_step():
    """Step 7: Implementation Projects"""
    if not st.session_state.selected_department:
        navigate_to_step('department_selection')
        return
    
    dept = st.session_state.selected_department
    dept_config = SHARED_SERVICE_DEPARTMENTS[dept]
    
    st.markdown(f"## 🚀 {dept_config['title']} - Implementation Projects")
    st.markdown("Define custom implementation projects and initiatives.")
    
    # Add new project
    with st.expander("Add New Implementation Project", expanded=True):
        with st.form(f"new_project_{dept}"):
            col1, col2 = st.columns(2)
            
            with col1:
                project_name = st.text_input("Project Name")
                project_description = st.text_area("Project Description")
                timeline = st.selectbox("Timeline", ["Q1 2025", "Q2 2025", "Q3 2025", "Q4 2025", "Multi-quarter"])
            
            with col2:
                budget = st.number_input("Budget (SAR)", min_value=0, value=100000, step=10000)
                priority = st.select_slider("Priority", ["Low", "Medium", "High", "Critical"], value="Medium")
                success_criteria = st.text_area("Success Criteria")
            
            if st.form_submit_button("Add Project", type="primary"):
                if project_name and project_description and budget > 0:
                    project = {
                        'name': project_name,
                        'description': project_description,
                        'timeline': timeline,
                        'budget': budget,
                        'priority': priority,
                        'success_criteria': success_criteria,
                        'created_date': datetime.now().strftime("%Y-%m-%d")
                    }
                    st.session_state.implementation_projects[dept].append(project)
                    st.success(f"✅ Added project: {project_name}")
                    st.rerun()
                else:
                    st.error("Please fill in all required fields.")
    
    # Display existing projects
    if st.session_state.implementation_projects[dept]:
        st.markdown("### Your Implementation Projects")
        
        for i, project in enumerate(st.session_state.implementation_projects[dept]):
            priority_colors = {
                'Low': '#10b981',
                'Medium': '#f59e0b',
                'High': '#ef4444',
                'Critical': '#dc2626'
            }
            
            priority_color = priority_colors.get(project['priority'], '#6b7280')
            
            st.markdown(f"""
            <div class='service-card' style='border-left: 4px solid {priority_color};'>
                <div style='display: flex; justify-content: space-between; align-items: start;'>
                    <div style='flex: 1;'>
                        <h4>{project['name']}</h4>
                        <p style='color: #6b7280; margin: 0.5rem 0;'><strong>Timeline:</strong> {project['timeline']}</p>
                        <p style='color: {priority_color}; margin: 0.5rem 0;'><strong>Priority:</strong> {project['priority']}</p>
                        <p style='margin: 0.5rem 0;'>{project['description']}</p>
                        {f"<p style='margin: 0.5rem 0;'><strong>Success Criteria:</strong> {project['success_criteria']}</p>" if project['success_criteria'] else ""}
                    </div>
                    <div style='text-align: right; margin-left: 1rem;'>
                        <h3 style='color: #1f2937; margin: 0;'>SAR {project['budget']:,.0f}</h3>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Remove {project['name']}", key=f"remove_project_{dept}_{i}"):
                st.session_state.implementation_projects[dept].pop(i)
                st.rerun()
    
    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Support", use_container_width=True):
            navigate_to_step('support')
    with col2:
        if st.button("Continue to Summary →", type="primary", use_container_width=True):
            navigate_to_step('summary')

def show_summary_step():
    """Step 8: Summary and Submission"""
    if not st.session_state.selected_department:
        navigate_to_step('department_selection')
        return
    
    dept = st.session_state.selected_department
    dept_config = SHARED_SERVICE_DEPARTMENTS[dept]
    
    st.markdown(f"## 📊 {dept_config['title']} - Budget Summary")
    st.markdown("Review your complete service selection and submit your budget request.")
    
    # Calculate totals
    operational_total = calculate_operational_total()
    support_total = calculate_support_total()
    project_total = calculate_project_total()
    total_budget = operational_total + support_total + project_total
    
    # Budget overview
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
    
    # Budget breakdown visualization
    if total_budget > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            fig_pie = px.pie(
                values=[operational_total, support_total, project_total],
                names=['Operational Services', 'Support Package', 'Implementation Projects'],
                title=f"{dept_config['title']} Budget Distribution",
                color_discrete_sequence=[dept_config['color'], '#10b981', '#f59e0b']
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Monthly cash flow
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            monthly_costs = [0] * 12
            monthly_costs[11] = operational_total + support_total  # Year-end billing
            
            # Distribute project costs based on timeline
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
                title="Monthly Cash Flow Projection",
                labels={'y': 'Cost (SAR)', 'x': 'Month'}
            )
            fig_bar.update_traces(marker_color=dept_config['color'])
            st.plotly_chart(fig_bar, use_container_width=True)
    
    # Detailed breakdown
    st.markdown("### 📋 Detailed Selection Summary")
    
    # Operational services
    if operational_total > 0:
        st.markdown("#### 🛍️ Selected Operational Services")
        for service_key, data in st.session_state.operational_services[dept].items():
            if data.get('selected', False):
                st.markdown(f"• **{service_key.replace('_', ' ').title()}** - SAR {data.get('annual_cost', 0):,.0f}")
        
        for service in st.session_state.custom_services[dept]:
            st.markdown(f"• **{service['name']}** (Custom) - SAR {service['annual_cost']:,.0f}")
    
    # Support package
    if support_total > 0:
        package = st.session_state.support_packages[dept]
        st.markdown(f"#### 🛠️ Support Package: {package}")
        st.markdown(f"• **{package} Package** - SAR {support_total:,.0f}")
    
    # Projects
    if project_total > 0:
        st.markdown("#### 🚀 Implementation Projects")
        for project in st.session_state.implementation_projects[dept]:
            st.markdown(f"• **{project['name']}** ({project['timeline']}) - SAR {project['budget']:,.0f}")
    
    # Budget submission terms
    st.markdown("---")
    st.markdown("### 📋 Budget Submission Terms")
    
    if not st.session_state.terms_accepted.get('budget_submission', False):
        st.markdown("""
        <div class='terms-card'>
            <h4>Budget Submission Legal Framework</h4>
            <div style='background: white; padding: 1rem; border-radius: 8px; margin: 1rem 0; max-height: 200px; overflow-y: auto;'>
                <p><strong>Authority Confirmation:</strong> I confirm that I have the authority to commit company resources for the selected services.</p>
                <p><strong>Budget Accuracy:</strong> I warrant that the budget information provided is accurate to the best of my knowledge.</p>
                <p><strong>Funding Commitment:</strong> My company commits to funding the approved services as outlined in this submission.</p>
                <p><strong>Contract Formation:</strong> I understand that budget approval creates binding service obligations.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("❌ Decline Terms", use_container_width=True):
                st.error("Budget submission terms must be accepted to proceed.")
        with col2:
            if st.button("✅ Accept Submission Terms", use_container_width=True, type="primary"):
                st.session_state.terms_accepted['budget_submission'] = True
                st.success("✅ Budget submission terms accepted!")
                st.rerun()
    else:
        # Export and submission options
        st.markdown("### 📤 Export & Submit")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📊 Export to Excel", use_container_width=True):
                st.success("📊 Excel export functionality would generate a comprehensive budget report.")
        
        with col2:
            if st.button("💾 Save Draft", use_container_width=True):
                st.success("💾 Draft saved successfully!")
        
        with col3:
            if st.button("📧 Share Summary", use_container_width=True):
                st.success("📧 Budget summary prepared for sharing.")
        
        with col4:
            if st.button("🚀 Submit Final Budget", type="primary", use_container_width=True):
                # Generate submission confirmation
                company_code = st.session_state.company_info.get('company', 'ALK')
                dept_code = dept[:3].upper()
                reference_id = f"{company_code}-{dept_code}-2025-{datetime.now().strftime('%Y%m%d%H%M%S')}"
                
                st.balloons()
                st.success(f"""
                ✅ **Budget Successfully Submitted!**
                
                **Reference ID:** {reference_id}
                
                **Submission Summary:**
                - Company: {st.session_state.company_info.get('company', 'N/A')}
                - Department: {dept_config['title']}
                - Contact: {st.session_state.company_info.get('contact_person', 'N/A')}
                - Total Budget: SAR {total_budget:,.0f}
                
                **Next Steps:**
                1. {dept_config['title']} team review (3-5 business days)
                2. Finance approval process
                3. Implementation planning begins
                4. Service delivery starts Q1 2025
                
                A detailed report has been sent to your email and the shared services team.
                """)
    
    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Projects", use_container_width=True):
            navigate_to_step('projects')
    with col2:
        if st.button("🔄 Start New Department", use_container_width=True):
            st.session_state.selected_department = None
            navigate_to_step('department_selection')

# ==================== ADMIN FUNCTIONS ====================

def show_admin_login():
    """Show admin login interface"""
    st.markdown("""
    <div style='max-width: 400px; margin: 2rem auto; background: white; border: 2px solid #e5e7eb; border-radius: 12px; padding: 2rem; box-shadow: 0 4px 12px rgba(0,0,0,0.1);'>
        <h2 style='text-align: center; color: #dc2626; margin-bottom: 1.5rem;'>
            🔐 Department Head Access
        </h2>
        <p style='text-align: center; color: #6b7280; margin-bottom: 1.5rem;'>
            Secure access for Department Heads to manage shared services content and pricing.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("admin_login_form"):
        st.markdown("### Login Credentials")
        username = st.text_input("Username", placeholder="e.g., it_admin")
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
    
    # Demo credentials
    with st.expander("🔍 Demo Credentials"):
        st.markdown("""
        **For demonstration purposes:**
        
        - **IT Admin:** `it_admin` / `itadmin2025`
        - **HR Admin:** `hr_admin` / `hradmin2025`
        - **Legal Admin:** `legal_admin` / `legaladmin2025`
        - **Procurement Admin:** `procurement_admin` / `procadmin2025`
        - **Facility Admin:** `facility_admin` / `faciladmin2025`
        - **Super Admin:** `super_admin` / `superadmin2025`
        """)

def show_admin_dashboard():
    """Show admin dashboard"""
    admin_info = st.session_state.get('admin_info', {})
    admin_dept = admin_info.get('department', '')
    
    if admin_dept == 'ALL':
        show_super_admin_dashboard()
    else:
        show_department_admin_dashboard(admin_dept)

def show_super_admin_dashboard():
    """Show super admin dashboard"""
    st.markdown("## 🔧 Super Administrator Dashboard")
    
    tabs = st.tabs(["📊 Overview", "🛠️ Services", "📋 Terms", "👥 Users"])
    
    with tabs[0]:
        st.markdown("### System Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            total_services = sum(len(services) for services in st.session_state.admin_services.values())
            st.metric("Total Services", total_services)
        with col2:
            st.metric("Support Packages", len(st.session_state.admin_support_packages))
        with col3:
            st.metric("Departments", len(SHARED_SERVICE_DEPARTMENTS))
        with col4:
            st.metric("Admin Users", len(ADMIN_CREDENTIALS))
    
    with tabs[1]:
        show_services_management()
    
    with tabs[2]:
        show_terms_management()
    
    with tabs[3]:
        show_user_management()

def show_department_admin_dashboard(department):
    """Show department-specific admin dashboard"""
    dept_config = SHARED_SERVICE_DEPARTMENTS.get(department, {})
    
    st.markdown(f"## {dept_config.get('icon', '🔧')} {dept_config.get('title', department)} Administration")
    
    tabs = st.tabs(["🛠️ Services", "📋 Terms", "📊 Analytics"])
    
    with tabs[0]:
        show_department_services_management(department)
    
    with tabs[1]:
        show_department_terms_management(department)
    
    with tabs[2]:
        show_department_analytics(department)

def show_services_management():
    """Show services management interface"""
    st.markdown("### 🛠️ Services Management")
    
    for dept, dept_config in SHARED_SERVICE_DEPARTMENTS.items():
        with st.expander(f"{dept_config['icon']} {dept_config['title']} Services"):
            services = st.session_state.admin_services[dept]
            
            # Add new service
            with st.form(f"add_service_{dept}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    service_name = st.text_input("Service Name", key=f"name_{dept}")
                    description = st.text_area("Description", key=f"desc_{dept}")
                
                with col2:
                    price = st.number_input("Price per Unit", min_value=0, value=100, key=f"price_{dept}")
                    setup_cost = st.number_input("Setup Cost", min_value=0, value=5000, key=f"setup_{dept}")
                
                with col3:
                    st.markdown("**Pricing Model:**")
                    if dept == "IT":
                        pricing_key = "price_per_user"
                    elif dept == "HR":
                        pricing_key = "price_per_user"
                    elif dept == "Legal":
                        pricing_key = "price_per_contract"
                    elif dept == "Procurement":
                        pricing_key = "price_per_transaction"
                    else:  # Facility_Safety
                        pricing_key = "price_per_sq_meter"
                    
                    st.info(f"Using: {pricing_key.replace('_', ' ').title()}")
                
                if st.form_submit_button(f"Add {dept_config['title']} Service"):
                    if service_name and description:
                        st.session_state.admin_services[dept][service_name] = {
                            pricing_key: price,
                            'setup_cost': setup_cost,
                            'description': description
                        }
                        st.success(f"✅ Added {service_name} to {dept_config['title']}")
                        st.rerun()
            
            # Existing services
            for service_name, details in services.items():
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    st.markdown(f"**{service_name}**")
                    st.markdown(f"*{details['description']}*")
                
                with col2:
                    pricing_key = next(k for k in details.keys() if k.startswith('price_per_'))
                    st.markdown(f"**Price:** SAR {details[pricing_key]} per {pricing_key.replace('price_per_', '').replace('_', ' ')}")
                    st.markdown(f"**Setup:** SAR {details['setup_cost']:,}")
                
                with col3:
                    if st.button("🗑️ Remove", key=f"remove_{dept}_{service_name}"):
                        del st.session_state.admin_services[dept][service_name]
                        st.rerun()

def show_terms_management():
    """Show terms management interface"""
    st.markdown("### 📋 Terms & Conditions Management")
    
    for terms_key, terms_data in st.session_state.admin_terms.items():
        with st.expander(f"✏️ {terms_data['title']}"):
            new_title = st.text_input("Title", value=terms_data['title'], key=f"title_{terms_key}")
            new_content = st.text_area("Content", value=terms_data['content'], height=200, key=f"content_{terms_key}")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Update Terms", key=f"update_{terms_key}"):
                    st.session_state.admin_terms[terms_key] = {
                        'title': new_title,
                        'content': new_content
                    }
                    st.success(f"✅ Updated {terms_data['title']}")
                    st.rerun()
            
            with col2:
                if st.button("👁️ Preview", key=f"preview_{terms_key}"):
                    st.markdown(f"**Preview: {new_title}**")
                    st.markdown(new_content)

def show_user_management():
    """Show user management interface"""
    st.markdown("### 👥 User Management")
    
    # Display admin users
    for username, details in ADMIN_CREDENTIALS.items():
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            st.markdown(f"**{details['name']}**")
            st.markdown(f"Username: `{username}`")
        
        with col2:
            st.markdown(f"**Department:** {details['department']}")
            st.markdown(f"**Access Level:** {'Super Admin' if details['department'] == 'ALL' else 'Department Head'}")
        
        with col3:
            status = "🟢 Active" if username == st.session_state.get('admin_user') else "⚪ Inactive"
            st.markdown(status)

def show_department_services_management(department):
    """Show department-specific services management"""
    services = st.session_state.admin_services[department]
    dept_config = SHARED_SERVICE_DEPARTMENTS[department]
    
    st.markdown(f"### {dept_config['icon']} {dept_config['title']} Services")
    
    # Service statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Services", len(services))
    with col2:
        avg_price = sum(list(service.values())[0] for service in services.values() if services) / len(services) if services else 0
        st.metric("Avg Price", f"SAR {avg_price:.0f}")
    with col3:
        total_setup = sum(service['setup_cost'] for service in services.values())
        st.metric("Total Setup Costs", f"SAR {total_setup:,}")
    
    # Service management (similar to super admin but department-specific)
    show_services_management()

def show_department_terms_management(department):
    """Show department-specific terms management"""
    st.markdown(f"### ⚖️ {SHARED_SERVICE_DEPARTMENTS[department]['title']} Terms")
    
    terms_key = department
    if terms_key in st.session_state.admin_terms:
        terms_data = st.session_state.admin_terms[terms_key]
        
        new_title = st.text_input("Terms Title", value=terms_data['title'])
        new_content = st.text_area("Terms Content", value=terms_data['content'], height=300)
        
        if st.button("💾 Update Department Terms", type="primary"):
            st.session_state.admin_terms[terms_key] = {
                'title': new_title,
                'content': new_content
            }
            st.success("✅ Department terms updated successfully!")
            st.rerun()

def show_department_analytics(department):
    """Show department analytics"""
    st.markdown(f"### 📊 {SHARED_SERVICE_DEPARTMENTS[department]['title']} Analytics")
    
    # Simulated analytics data
    services = st.session_state.admin_services[department]
    
    if services:
        # Service popularity chart
        service_names = list(services.keys())
        popularity_scores = [len(name) * 10 + 50 for name in service_names]  # Simulated data
        
        fig = px.bar(x=service_names, y=popularity_scores, title="Service Popularity")
        st.plotly_chart(fig, use_container_width=True)
        
        # Pricing analysis
        prices = [list(service.values())[0] for service in services.values()]
        fig2 = px.histogram(x=prices, title="Price Distribution", nbins=10)
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No services configured yet for analytics.")

# ==================== MAIN APPLICATION ====================

def main():
    """Main application entry point"""
    # Initialize session state
    initialize_session_state()
    
    # Show header
    show_header()
    
    # Show sidebar
    show_sidebar()
    
    # Check application mode
    app_mode = st.session_state.get('app_mode', 'client')
    
    if app_mode == 'admin':
        # Admin mode
        if not st.session_state.get('admin_authenticated', False):
            show_admin_login()
        else:
            show_admin_dashboard()
    else:
        # Client mode
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
        elif current_step == 'summary':
            show_summary_step()
        else:
            # Default to company info
            show_company_info_step()

if __name__ == "__main__":
    main()