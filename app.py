import streamlit as st
from database import (
    check_user_status, save_user_data, get_all_alumni, 
    post_job, get_all_jobs
)

st.set_page_config(page_title="Alumni Nexus", page_icon="🎓", layout="centered")

# Initialize Session States
if 'step' not in st.session_state:
    st.session_state.step = "id_check"
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- PHASE 1: LOGIN / SIGNUP ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>🎓 Alumni Nexus</h1>", unsafe_allow_html=True)
    
    if st.session_state.step == "id_check":
        reg_input = st.text_input("Registration Number", placeholder="e.g., 25E104B90")
        if st.button("Continue"):
            if reg_input:
                user = check_user_status(reg_input)
                st.session_state.temp_id = reg_input
                if user and user.get('password'):
                    st.session_state.step = "login"
                else:
                    st.session_state.step = "onboarding"
                st.rerun()

    elif st.session_state.step == "onboarding":
        st.subheader("🆕 Complete Your Profile")
        name = st.text_input("Full Name")
        branch = st.selectbox("Branch", ["ECE", "CSE", "ME", "EE", "CE"])
        new_pass = st.text_input("Create Password", type="password")
        if st.button("Finish Setup"):
            if name and new_pass:
                save_user_data(st.session_state.temp_id, name, branch, new_pass, True)
                st.session_state.step = "login"
                st.rerun()

    elif st.session_state.step == "login":
        st.subheader("Welcome Back!")
        login_pass = st.text_input("Password", type="password")
        if st.button("Login"):
            user = check_user_status(st.session_state.temp_id)
            # FIXED LOGIC: Safe access to dictionary keys
            if user and login_pass == user['password']:
                st.session_state.logged_in = True
                st.session_state.user_name = user['full_name']
                st.session_state.user_branch = user.get('branch', 'N/A')
                st.rerun()
            else:
                st.error("Invalid Password")
        
        if st.button("Back to ID Check"):
            st.session_state.step = "id_check"
            st.rerun()

# --- PHASE 2: DASHBOARD ---
else:
    st.sidebar.title(f"👤 {st.session_state.user_name}")
    menu = st.sidebar.radio("Navigation", ["Home", "Search Alumni", "Job Board", "My Profile"])
    
    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()
#for home page, we will create a dashboard with 4 sections: Networking Opportunities, Career Development, Exclusive Events, and Give Back. Each section will have a brief description and a call-to-action button that guides users to the relevant part of the platform.
    if menu == "Home":
        # ... (Pehle wala dashboard cards ka code yahan rahega) ...

        st.write("---")
        
        # Alumni Counter Section
        from database import get_total_alumni_count
        total_registered = get_total_alumni_count()
        
        st.markdown(f"""
            <div style="text-align: center; padding: 20px; background-color: #f0f2f6; border-radius: 10px; margin-top: 20px;">
                <h2 style="color: #4e73df; margin-bottom: 0;">🧑 {total_registered}</h2>
                <p style="font-size: 18px; color: #5a5c69;">Alumni already registered in our Network</p>
            </div>
        """, unsafe_allow_html=True)
        # Row 1: Networking & Career
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
                <div style="background-color: #f8f9fa; padding: 25px; border-radius: 15px; border-top: 5px solid #4e73df; min-height: 200px;">
                    <h3 style="color: #4e73df;">👥 Networking Opportunities</h3>
                    <p>Connect with fellow alumni across different industries and regions.</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Browse Directory", use_container_width=True):
                st.info("Select from side menu!")

        with col2:
            st.markdown("""
                <div style="background-color: #f8f9fa; padding: 25px; border-radius: 15px; border-top: 5px solid #1cc88a; min-height: 200px;">
                    <h3 style="color: #1cc88a;">💼 Career Development</h3>
                    <p>Access job postings, referral programs, and career resources.</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("View Job Board", use_container_width=True):
                st.info("Select from side menu!")

        st.write("") # Spacing

        # Row 2: Events & Give Back
        col3, col4 = st.columns(2)
        with col3:
            st.markdown("""
                <div style="background-color: #f8f9fa; padding: 25px; border-radius: 15px; border-top: 5px solid #f6c23e; min-height: 200px;">
                    <h3 style="color: #f6c23e;">🏅 Exclusive Events</h3>
                    <p>Attend alumni reunions, workshops, and professional development sessions.</p>
                </div>
            """, unsafe_allow_html=True)
            st.button("Upcoming Events", use_container_width=True, disabled=True)

        with col4:
            st.markdown("""
                <div style="background-color: #f8f9fa; padding: 25px; border-radius: 15px; border-top: 5px solid #e74a3b; min-height: 200px;">
                    <h3 style="color: #e74a3b;">🤝 Give Back</h3>
                    <p>Mentor current students and contribute to the growth of the community.</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Become a Mentor", use_container_width=True):
                st.info("Go to 'My Profile' and enable Mentorship toggle!")
#job board section , users can post new job referrals and view existing ones. Each job referral will display the job title, company, description, and an optional link to apply. Users can click on the "Apply Now" button to be redirected to the application page.
    elif menu == "Job Board":
        st.title("💼 Job Referrals")
        with st.expander("Post a New Job/Internship"):
            t = st.text_input("Job Title")
            c = st.text_input("Company")
            d = st.text_area("Description")
            l = st.text_input("Apply Link")
            if st.button("Post"):
                if post_job(t, c, d, st.session_state.temp_id, l):
                    st.success("Posted successfully!")
                    st.rerun()
        
        jobs = get_all_jobs()
        for j in jobs:
            st.subheader(f"{j['title']} @ {j['company']}")
            st.write(j['description'])
            if j['link']: st.link_button("Apply Now", j['link'])
            st.divider()
    elif menu == "Search Alumni":
        st.title("🔍 Alumni Directory")
        st.write("Find and connect with fellow graduates and mentors.")

        # 1. Fetch Data
        alumni_list = get_all_alumni()

        if alumni_list:
            # 2. Search & Filter UI
            col1, col2 = st.columns([2, 1])
            with col1:
                search_query = st.text_input("Search by Name", placeholder="Enter name...")
            with col2:
                st.write("") # Alignment
                show_mentors = st.toggle("Mentors Only 🎓")

            # 3. Apply Filters
            filtered_data = [
                p for p in alumni_list 
                if (search_query.lower() in p.get('full_name', '').lower()) and
                   (not show_mentors or p.get('is_mentor') == 1)
            ]

            # 4. Display Table
            if filtered_data:
                # Improving column labels for the UI
                import pandas as pd
                df = pd.DataFrame(filtered_data)
                # Change line 175 in app.py to this:
                df.columns = ["Reg No", "Name", "Branch", "Email", "LinkedIn", "Is Mentor"]
                
                st.dataframe(
                    df, 
                    use_container_width=True,
                    column_config={
                        "LinkedIn": st.column_config.LinkColumn("LinkedIn Profile")
                    }
                )
            else:
                st.warning("No alumni found matching your search.")
        else:
            st.info("The directory is currently empty. Be the first to join!")  

    elif menu == "My Profile":
        st.title("👤 My Professional Profile")
        user = check_user_status(st.session_state.temp_id)
        if user:
            # Indented correctly inside 'with' block to fix previous crash
            with st.form("profile_editor"):
                u_email = st.text_input("Email", value=user.get('email') or "")
                u_linkedin = st.text_input("LinkedIn URL", value=user.get('linkedin_id') or "")
                u_intro = st.text_area("Short Bio", value=user.get('intro') or "")
                u_mentor = st.checkbox("Willing to Mentor?", value=bool(user.get('is_mentor')))
                
                if st.form_submit_button("Save Changes"):
                    save_user_data(st.session_state.temp_id, user['full_name'], user['branch'], 
                                   user['password'], False, u_linkedin, u_intro, u_email, int(u_mentor))
                    st.success("Profile Updated!")
                    st.rerun()
            
            st.divider()
            st.write(f"**Verified ID:** {user['reg_no']}")
        st.divider()
    st.markdown("""
    <div style='text-align: center; color: grey;'>
        Built with ❤️ by Divyansh |  2026 Alumni Nexus
    </div>
""", unsafe_allow_html=True)
#streamlit run app.py

