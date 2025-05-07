# Import packages
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import mysql.connector

def connect_db():
    try:
        import mysql.connector
        conn = mysql.connector.connect(
            host="localhost",
            user="cs7330",
            password="pw7330",
            database="finalproject"
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Failed to connect: {err}")
        return None

# Create the main window
class SocialMediaAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Social Media Analysis")
        self.root.geometry("1000x800")

        # Initialize database connection
        self.connection = connect_db()
        if self.connection:
            self.cursor = self.connection.cursor(dictionary=True)
        else:
            messagebox.showerror("Error", "Could not connect to database. Please check your credentials.")
            exit(1)

        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Create tabs
        self.create_project_tab()
        self.create_fields_tab()
        self.create_posts_tab()
        self.create_analysis_tab()
        self.create_query_tab()
        self.create_experiment_tab()
        self.create_combined_query_tab()  # 7330 requirement

        # Populate dropdowns
        self.populate_project_dropdown()
    # TABS
    def create_project_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Project Information")

        # Project fields
        ttk.Label(tab, text="Project Information", font=("Arial", 14)).grid(row=0, column=0, columnspan=2, pady=10,
                                                                            padx=10)

        ttk.Label(tab, text="Project Name:").grid(row=1, column=0, pady=5, padx=5, sticky="e")
        self.project_name = ttk.Entry(tab, width=40)
        self.project_name.grid(row=1, column=1, pady=5, padx=5)

        ttk.Label(tab, text="Project Manager First Name:").grid(row=2, column=0, pady=5, padx=5, sticky="e")
        self.manager_fname = ttk.Entry(tab, width=40)
        self.manager_fname.grid(row=2, column=1, pady=5, padx=5)

        ttk.Label(tab, text="Project Manager Last Name:").grid(row=3, column=0, pady=5, padx=5, sticky="e")
        self.manager_lname = ttk.Entry(tab, width=40)
        self.manager_lname.grid(row=3, column=1, pady=5, padx=5)

        ttk.Label(tab, text="Institution Name:").grid(row=4, column=0, pady=5, padx=5, sticky="e")
        self.institution = ttk.Entry(tab, width=40)
        self.institution.grid(row=4, column=1, pady=5, padx=5)

        ttk.Label(tab, text="Start Date (YYYY-MM-DD):").grid(row=5, column=0, pady=5, padx=5, sticky="e")
        self.start_date = ttk.Entry(tab, width=40)
        self.start_date.grid(row=5, column=1, pady=5, padx=5)

        ttk.Label(tab, text="End Date (YYYY-MM-DD):").grid(row=6, column=0, pady=5, padx=5, sticky="e")
        self.end_date = ttk.Entry(tab, width=40)
        self.end_date.grid(row=6, column=1, pady=5, padx=5)

        # Save button
        self.save_project_button = ttk.Button(tab, text="Save Project", command=self.save_project)
        self.save_project_button.grid(row=7, column=0, columnspan=2, pady=20)
        # Create a frame for utility buttons
        utility_frame = ttk.Frame(tab)
        utility_frame.grid(row=8, column=0, columnspan=2, pady=10)

        # Add Sample Data button
        sample_data_button = ttk.Button(utility_frame, text="Add Sample Dataset",
                                        command=self.populate_sample_data)
        sample_data_button.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

        # You can also add your reset buttons here if you want them all together
        reset_projects_btn = ttk.Button(utility_frame, text="Reset Project Data", command=self.reset_project_data)
        reset_projects_btn.grid(row=0, column=1, padx=5, pady=5)

        reset_all_btn = ttk.Button(utility_frame, text="Reset All Data", command=self.reset_all_data)
        reset_all_btn.grid(row=0, column=2, padx=5, pady=5)
    def create_fields_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Project Fields")

        ttk.Label(tab, text="Manage Project Fields", font=("Arial", 14)).grid(row=0, column=0, columnspan=2, pady=10,
                                                                              padx=10)

        ttk.Label(tab, text="Select Project:").grid(row=1, column=0, pady=5, padx=5, sticky="e")
        self.project_field_dropdown = ttk.Combobox(tab, width=40)
        self.project_field_dropdown.grid(row=1, column=1, pady=5, padx=5)

        ttk.Label(tab, text="New Field Name:").grid(row=2, column=0, pady=5, padx=5, sticky="e")
        self.new_field_name = ttk.Entry(tab, width=40)
        self.new_field_name.grid(row=2, column=1, pady=5, padx=5)

        # Add button
        self.add_field_button = ttk.Button(tab, text="Add Field to Project", command=self.add_project_field)
        self.add_field_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Field list
        ttk.Label(tab, text="Current Fields:").grid(row=4, column=0, columnspan=2, pady=10, padx=5, sticky="w")

        self.fields_tree = ttk.Treeview(tab, columns=("Project", "Field"), show="headings")
        self.fields_tree.heading("Project", text="Project")
        self.fields_tree.heading("Field", text="Field Name")
        self.fields_tree.grid(row=5, column=0, columnspan=2, pady=5, padx=10, sticky="nsew")

        # Configure row and column weights
        tab.grid_rowconfigure(5, weight=1)
        tab.grid_columnconfigure(1, weight=1)

        # Bind project selection to load fields
        self.project_field_dropdown.bind('<<ComboboxSelected>>', self.load_project_fields)
    def create_posts_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Associate Posts")

        ttk.Label(tab, text="Associate Posts with Projects", font=("Arial", 14)).grid(row=0, column=0, columnspan=4,
                                                                                      pady=10, padx=10)

        ttk.Label(tab, text="Select Project:").grid(row=1, column=0, pady=5, padx=5, sticky="e")
        self.project_dropdown = ttk.Combobox(tab, width=40)
        self.project_dropdown.grid(row=1, column=1, pady=5, padx=5, columnspan=3)

        ttk.Separator(tab, orient="horizontal").grid(row=2, column=0, columnspan=4, sticky="ew", pady=10)

        # User Info Frame
        user_frame = ttk.LabelFrame(tab, text="User Information")
        user_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="nw")

        ttk.Label(user_frame, text="Social Media:").grid(row=0, column=0, pady=5, padx=5, sticky="e")
        self.social_media = ttk.Combobox(user_frame, width=25, values=["Facebook", "Twitter", "Instagram"])
        self.social_media.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(user_frame, text="Username:").grid(row=1, column=0, pady=5, padx=5, sticky="e")
        self.username = ttk.Entry(user_frame, width=25)
        self.username.grid(row=1, column=1, pady=5, padx=5)

        ttk.Label(user_frame, text="First Name:").grid(row=2, column=0, pady=5, padx=5, sticky="e")
        self.user_fname = ttk.Entry(user_frame, width=25)
        self.user_fname.grid(row=2, column=1, pady=5, padx=5)

        ttk.Label(user_frame, text="Last Name:").grid(row=3, column=0, pady=5, padx=5, sticky="e")
        self.user_lname = ttk.Entry(user_frame, width=25)
        self.user_lname.grid(row=3, column=1, pady=5, padx=5)

        ttk.Label(user_frame, text="Country of Birth:").grid(row=4, column=0, pady=5, padx=5, sticky="e")
        self.birth_country = ttk.Entry(user_frame, width=25)
        self.birth_country.grid(row=4, column=1, pady=5, padx=5)

        ttk.Label(user_frame, text="Country of Residence:").grid(row=5, column=0, pady=5, padx=5, sticky="e")
        self.residence_country = ttk.Entry(user_frame, width=25)
        self.residence_country.grid(row=5, column=1, pady=5, padx=5)

        ttk.Label(user_frame, text="Age:").grid(row=6, column=0, pady=5, padx=5, sticky="e")
        self.age = ttk.Entry(user_frame, width=25)
        self.age.grid(row=6, column=1, pady=5, padx=5)

        ttk.Label(user_frame, text="Gender:").grid(row=7, column=0, pady=5, padx=5, sticky="e")
        self.gender = ttk.Entry(user_frame, width=25)
        self.gender.grid(row=7, column=1, pady=5, padx=5)

        ttk.Label(user_frame, text="Verified User:").grid(row=8, column=0, pady=5, padx=5, sticky="e")
        self.verified_var = tk.BooleanVar()
        self.verified_check = ttk.Checkbutton(user_frame, variable=self.verified_var)
        self.verified_check.grid(row=8, column=1, pady=5, padx=5, sticky="w")

        # Post Info Frame
        post_frame = ttk.LabelFrame(tab, text="Post Information")
        post_frame.grid(row=3, column=2, columnspan=2, padx=10, pady=5, sticky="nw")

        ttk.Label(post_frame, text="Post Time (YYYY-MM-DD HH:MM):").grid(row=0, column=0, pady=5, padx=5, sticky="e")
        self.post_time = ttk.Entry(post_frame, width=25)
        self.post_time.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(post_frame, text="City:").grid(row=1, column=0, pady=5, padx=5, sticky="e")
        self.city = ttk.Entry(post_frame, width=25)
        self.city.grid(row=1, column=1, pady=5, padx=5)

        ttk.Label(post_frame, text="State:").grid(row=2, column=0, pady=5, padx=5, sticky="e")
        self.state = ttk.Entry(post_frame, width=25)
        self.state.grid(row=2, column=1, pady=5, padx=5)

        ttk.Label(post_frame, text="Country:").grid(row=3, column=0, pady=5, padx=5, sticky="e")
        self.country = ttk.Entry(post_frame, width=25)
        self.country.grid(row=3, column=1, pady=5, padx=5)

        ttk.Label(post_frame, text="Likes:").grid(row=4, column=0, pady=5, padx=5, sticky="e")
        self.likes = ttk.Entry(post_frame, width=25)
        self.likes.grid(row=4, column=1, pady=5, padx=5)

        ttk.Label(post_frame, text="Dislikes:").grid(row=5, column=0, pady=5, padx=5, sticky="e")
        self.dislikes = ttk.Entry(post_frame, width=25)
        self.dislikes.grid(row=5, column=1, pady=5, padx=5)

        ttk.Label(post_frame, text="Has Multimedia:").grid(row=6, column=0, pady=5, padx=5, sticky="e")
        self.multimedia_var = tk.BooleanVar()
        self.multimedia_check = ttk.Checkbutton(post_frame, variable=self.multimedia_var)
        self.multimedia_check.grid(row=6, column=1, pady=5, padx=5, sticky="w")

        # Repost Frame
        repost_frame = ttk.LabelFrame(post_frame, text="Repost Information (Optional)")
        repost_frame.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        ttk.Label(repost_frame, text="Reposted by (Username):").grid(row=0, column=0, pady=5, padx=5, sticky="e")
        self.repost_username = ttk.Entry(repost_frame, width=25)
        self.repost_username.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(repost_frame, text="Repost Time (YYYY-MM-DD HH:MM):").grid(row=1, column=0, pady=5, padx=5,
                                                                             sticky="e")
        self.repost_time = ttk.Entry(repost_frame, width=25)
        self.repost_time.grid(row=1, column=1, pady=5, padx=5)

        # Post Text Frame
        post_text_frame = ttk.LabelFrame(tab, text="Post Text Content")
        post_text_frame.grid(row=4, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

        self.post_text = tk.Text(post_text_frame, width=80, height=8)
        self.post_text.grid(row=0, column=0, pady=5, padx=5)

        text_scroll = ttk.Scrollbar(post_text_frame, orient="vertical", command=self.post_text.yview)
        text_scroll.grid(row=0, column=1, sticky="ns")
        self.post_text.configure(yscrollcommand=text_scroll.set)

        # Save button
        self.save_post_button = ttk.Button(tab, text="Add Post to Project", command=self.save_post)
        self.save_post_button.grid(row=5, column=0, columnspan=4, pady=20)

        # List experiments button (7330 requirement)
        self.list_exp_button = ttk.Button(tab, text="List Experiments for Selected Posts",
                                          command=self.query_posts_then_experiments)
        self.list_exp_button.grid(row=6, column=0, columnspan=4, pady=5)
    def create_analysis_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Analysis Results")

        ttk.Label(tab, text="Enter Analysis Results", font=("Arial", 14)).grid(row=0, column=0, columnspan=2, pady=10,
                                                                               padx=10)

        ttk.Label(tab, text="Select Project:").grid(row=1, column=0, pady=5, padx=5, sticky="e")
        self.analysis_project = ttk.Combobox(tab, width=40)
        self.analysis_project.grid(row=1, column=1, pady=5, padx=5)

        ttk.Label(tab, text="Select Field:").grid(row=2, column=0, pady=5, padx=5, sticky="e")
        self.field_dropdown = ttk.Combobox(tab, width=40)
        self.field_dropdown.grid(row=2, column=1, pady=5, padx=5)

        ttk.Label(tab, text="Post ID:").grid(row=3, column=0, pady=5, padx=5, sticky="e")
        self.post_id = ttk.Entry(tab, width=40)
        self.post_id.grid(row=3, column=1, pady=5, padx=5)

        ttk.Label(tab, text="Field Value:").grid(row=4, column=0, pady=5, padx=5, sticky="e")
        self.field_value = ttk.Entry(tab, width=40)
        self.field_value.grid(row=4, column=1, pady=5, padx=5)

        # Save button
        self.save_analysis_button = ttk.Button(tab, text="Save Analysis Result", command=self.save_analysis)
        self.save_analysis_button.grid(row=5, column=0, columnspan=2, pady=20)

        # Bind project selection to populate fields
        self.analysis_project.bind('<<ComboboxSelected>>', self.populate_fields_dropdown)
    def create_query_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Query Posts")

        ttk.Label(tab, text="Query Posts by Criteria", font=("Arial", 14)).grid(row=0, column=0, columnspan=2, pady=10,
                                                                                padx=10)

        # Social Media Query
        sm_frame = ttk.LabelFrame(tab, text="Find Posts by Social Media")
        sm_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(sm_frame, text="Social Media:").grid(row=0, column=0, pady=5, padx=5, sticky="e")
        self.query_sm = ttk.Combobox(sm_frame, width=25, values=["Facebook", "Twitter", "Instagram"])
        self.query_sm.grid(row=0, column=1, pady=5, padx=5)

        sm_query_button = ttk.Button(sm_frame, text="Find Posts", command=self.query_by_social_media)
        sm_query_button.grid(row=1, column=0, columnspan=2, pady=10)

        # Date Range Query
        date_frame = ttk.LabelFrame(tab, text="Find Posts by Date Range")
        date_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(date_frame, text="Start Date (YYYY-MM-DD):").grid(row=0, column=0, pady=5, padx=5, sticky="e")
        self.query_start_date = ttk.Entry(date_frame, width=25)
        self.query_start_date.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(date_frame, text="End Date (YYYY-MM-DD):").grid(row=1, column=0, pady=5, padx=5, sticky="e")
        self.query_end_date = ttk.Entry(date_frame, width=25)
        self.query_end_date.grid(row=1, column=1, pady=5, padx=5)

        date_query_button = ttk.Button(date_frame, text="Find Posts", command=self.query_by_date_range)
        date_query_button.grid(row=2, column=0, columnspan=2, pady=10)

        # User Query
        user_query_frame = ttk.LabelFrame(tab, text="Find Posts by User")
        user_query_frame.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        ttk.Label(user_query_frame, text="Social Media:").grid(row=0, column=0, pady=5, padx=5, sticky="e")
        self.user_query_sm = ttk.Combobox(user_query_frame, width=25, values=["Facebook", "Twitter", "Instagram"])
        self.user_query_sm.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(user_query_frame, text="Username:").grid(row=1, column=0, pady=5, padx=5, sticky="e")
        self.user_query_name = ttk.Entry(user_query_frame, width=25)
        self.user_query_name.grid(row=1, column=1, pady=5, padx=5)

        user_query_button = ttk.Button(user_query_frame, text="Find Posts", command=self.query_by_user)
        user_query_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Name Query
        name_query_frame = ttk.LabelFrame(tab, text="Find Posts by Full Name")
        name_query_frame.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        ttk.Label(name_query_frame, text="First Name:").grid(row=0, column=0, pady=5, padx=5, sticky="e")
        self.first_name_query = ttk.Entry(name_query_frame, width=25)
        self.first_name_query.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(name_query_frame, text="Last Name:").grid(row=1, column=0, pady=5, padx=5, sticky="e")
        self.last_name_query = ttk.Entry(name_query_frame, width=25)
        self.last_name_query.grid(row=1, column=1, pady=5, padx=5)

        name_query_button = ttk.Button(name_query_frame, text="Find Posts", command=self.query_by_full_name)
        name_query_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Multimedia Query
        mm_query_frame = ttk.LabelFrame(tab, text="Find Posts by Multimedia")
        mm_query_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.mm_var = tk.BooleanVar()
        mm_check = ttk.Checkbutton(mm_query_frame, text="Has Multimedia", variable=self.mm_var)
        mm_check.grid(row=0, column=0, columnspan=2, pady=10)

        mm_query_button = ttk.Button(mm_query_frame, text="Find Posts", command=self.query_by_multimedia)
        mm_query_button.grid(row=1, column=0, columnspan=2, pady=10)

        # Results display area
        results_frame = ttk.LabelFrame(tab, text="Query Results")
        results_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.results_tree = ttk.Treeview(results_frame, columns=("ID", "Text", "Media", "User", "Time", "Experiments"),
                                         show="headings")
        self.results_tree.heading("ID", text="Post ID")
        self.results_tree.heading("Text", text="Post Text")
        self.results_tree.heading("Media", text="Social Media")
        self.results_tree.heading("User", text="Username")
        self.results_tree.heading("Time", text="Time Posted")
        self.results_tree.heading("Experiments", text="Experiments")

        self.results_tree.column("ID", width=50)
        self.results_tree.column("Text", width=300)
        self.results_tree.column("Media", width=100)
        self.results_tree.column("User", width=100)
        self.results_tree.column("Time", width=120)
        self.results_tree.column("Experiments", width=150)

        self.results_tree.pack(fill="both", expand=True, padx=5, pady=5)

        # Configure to make results area expandable
        tab.grid_rowconfigure(4, weight=1)
    def create_experiment_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Query Experiments")

        ttk.Label(tab, text="Query Experiments", font=("Arial", 14)).grid(row=0, column=0, columnspan=2, pady=10,
                                                                          padx=10)

        ttk.Label(tab, text="Experiment Name:").grid(row=1, column=0, pady=5, padx=5, sticky="e")
        self.exp_name_entry = ttk.Entry(tab, width=40)
        self.exp_name_entry.grid(row=1, column=1, pady=5, padx=5)

        # Query button
        exp_query_button = ttk.Button(tab, text="Query Experiment", command=self.query_experiment)
        exp_query_button.grid(row=2, column=0, columnspan=2, pady=20)

        # Results display area
        exp_results_frame = ttk.LabelFrame(tab, text="Experiment Results")
        exp_results_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.exp_results_tree = ttk.Treeview(exp_results_frame, columns=("Field", "Value", "Post", "Percentage"),
                                             show="headings")
        self.exp_results_tree.heading("Field", text="Field ID")
        self.exp_results_tree.heading("Value", text="Field Value")
        self.exp_results_tree.heading("Post", text="Post Text")
        self.exp_results_tree.heading("Percentage", text="Percentage")

        self.exp_results_tree.column("Field", width=80)
        self.exp_results_tree.column("Value", width=150)
        self.exp_results_tree.column("Post", width=400)
        self.exp_results_tree.column("Percentage", width=100)

        self.exp_results_tree.pack(fill="both", expand=True, padx=5, pady=5)

        # Configure to make results area expandable
        tab.grid_rowconfigure(3, weight=1)
    def create_combined_query_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Query Posts & Experiments")

        ttk.Label(tab, text="Query Posts then Experiments (7330 Requirement)", font=("Arial", 14)).grid(row=0, column=0,
                                                                                                        columnspan=2,
                                                                                                        pady=10,
                                                                                                        padx=10)

        ttk.Label(tab, text="Select Project:").grid(row=1, column=0, pady=5, padx=5, sticky="e")
        self.combined_project = ttk.Combobox(tab, width=40)
        self.combined_project.grid(row=1, column=1, pady=5, padx=5)

        # Query button
        combined_query_button = ttk.Button(tab, text="Find Posts & Experiments",
                                           command=self.query_posts_then_experiments)
        combined_query_button.grid(row=2, column=0, columnspan=2, pady=20)

        # Results display area
        combined_results_frame = ttk.LabelFrame(tab, text="Results")
        combined_results_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.combined_results_tree = ttk.Treeview(combined_results_frame,
                                                  columns=("ID", "Text", "Media", "User", "Time"), show="headings")
        self.combined_results_tree.heading("ID", text="Post ID")
        self.combined_results_tree.heading("Text", text="Post Text")
        self.combined_results_tree.heading("Media", text="Social Media")
        self.combined_results_tree.heading("User", text="Username")
        self.combined_results_tree.heading("Time", text="Time Posted")

        self.combined_results_tree.column("ID", width=50)
        self.combined_results_tree.column("Text", width=400)
        self.combined_results_tree.column("Media", width=100)
        self.combined_results_tree.column("User", width=100)
        self.combined_results_tree.column("Time", width=150)

        self.combined_results_tree.pack(fill="both", expand=True, padx=5, pady=5)

        # Configure to make results area expandable
        tab.grid_rowconfigure(3, weight=1)
    # FUNCTIONS
    def populate_sample_data(self):
        """Populate the database with a complete sample dataset"""
        try:
            cursor = self.connection.cursor()

            # First, add social media platforms
            social_media_data = [
                (1, "Twitter"),
                (2, "Instagram"),
                (3, "Facebook")
            ]

            for sm_id, sm_name in social_media_data:
                cursor.execute("SELECT ID FROM SocialMedia WHERE Name = %s", (sm_name,))
                if not cursor.fetchone():
                    cursor.execute("INSERT INTO SocialMedia (Name) VALUES (%s)", (sm_name,))
                    self.connection.commit()

            # Add institutions
            institutions = ["SMU", "University of Texas", "Texas A&M", "Rice University"]
            for institution in institutions:
                cursor.execute("SELECT Name FROM Institution WHERE Name = %s", (institution,))
                if not cursor.fetchone():
                    cursor.execute("INSERT INTO Institution (Name) VALUES (%s)", (institution,))
                    self.connection.commit()

            # Add users FIRST (important for foreign key constraints)
            user_data = [
                (1, "JohnDoe", "John", "Doe", "USA", "USA", 28, "Male", True),
                (2, "JaneSmith", "Jane", "Smith", "Canada", "USA", 32, "Female", True),
                (1, "TechGuru", "Alex", "Chen", "China", "USA", 35, "Male", True),
                (3, "FitnessFan", "Maria", "Garcia", "Mexico", "USA", 29, "Female", False),
                (2, "Traveler123", "Sam", "Wilson", "UK", "UK", 31, "Male", True),
                (3, "FoodLover", "Lisa", "Brown", "USA", "USA", 27, "Female", False),
                (1, "GamerPro", "Ryan", "Miller", "USA", "Canada", 24, "Male", True),
                (2, "ArtCreator", "Emma", "Davis", "France", "France", 33, "Female", True),
                (3, "SportsEnthusiast", "Michael", "Johnson", "USA", "USA", 30, "Male", False),
                (1, "MusicFan", "Olivia", "Taylor", "Australia", "USA", 26, "Female", True)
            ]

            # Make sure EACH user is committed to the database immediately
            for sm_id, username, first_name, last_name, birth_country, residence_country, age, gender, is_verified in user_data:
                # First check if the social media platform exists
                cursor.execute("SELECT ID FROM SocialMedia WHERE ID = %s", (sm_id,))
                if not cursor.fetchone():
                    messagebox.showerror("Error", f"Social Media with ID {sm_id} does not exist")
                    return

                # Then check if user already exists
                cursor.execute("SELECT ID FROM User WHERE SM_ID = %s AND Username = %s", (sm_id, username))
                if not cursor.fetchone():
                    cursor.execute("""
                        INSERT INTO User (SM_ID, Username, First_Name, Last_Name, Country_of_Birth, 
                        Country_of_Residence, Age, Gender, Is_Verified) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (sm_id, username, first_name, last_name, birth_country,
                          residence_country, age, gender, is_verified))
                    self.connection.commit()  # Commit each user separately to ensure it's saved

            # Add projects/experiments
            project_data = [
                ("Political Sentiment Analysis", "Robert", "Johnson", "SMU", "2023-01-01", "2023-12-31"),
                ("Brand Engagement Study", "Sarah", "Williams", "University of Texas", "2023-02-15", "2023-11-30"),
                ("COVID-19 Information Spread", "David", "Brown", "Texas A&M", "2023-03-10", "2023-10-15"),
                (
                "Environmental Awareness Campaign", "Jennifer", "Miller", "Rice University", "2023-04-20", "2023-09-30")
            ]

            project_ids = {}
            for name, pm_first, pm_last, institution, start_date, end_date in project_data:
                cursor.execute("SELECT ID FROM Project WHERE Name = %s", (name,))
                result = cursor.fetchone()
                if not result:
                    cursor.execute("""
                        INSERT INTO Project (Name, PM_First_Name, PM_Last_Name, Institution_Name, Start_Date, End_Date)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (name, pm_first, pm_last, institution, start_date, end_date))
                    self.connection.commit()
                    cursor.execute("SELECT LAST_INSERT_ID()")
                    project_ids[name] = cursor.fetchone()[0]
                else:
                    project_ids[name] = result[0]

            # Add project fields
            field_data = [
                ("Political Sentiment Analysis", [
                    "PostAssociation", "Sentiment", "Political_Leaning", "Topic", "Region"
                ]),
                ("Brand Engagement Study", [
                    "PostAssociation", "Sentiment", "Brand_Mentioned", "Engagement_Level", "Demographics"
                ]),
                ("COVID-19 Information Spread", [
                    "PostAssociation", "Information_Type", "Accuracy", "Source_Cited", "Reach"
                ]),
                ("Environmental Awareness Campaign", [
                    "PostAssociation", "Environmental_Issue", "Call_To_Action", "Target_Audience", "Geographic_Focus"
                ])
            ]

            field_ids = {}
            for project_name, fields in field_data:
                project_id = project_ids[project_name]
                for field_name in fields:
                    cursor.execute("""
                        SELECT ID FROM ProjectFields
                        WHERE Project_ID = %s AND Field_Name = %s
                    """, (project_id, field_name))
                    result = cursor.fetchone()
                    if not result:
                        cursor.execute("""
                            INSERT INTO ProjectFields (Project_ID, Field_Name)
                            VALUES (%s, %s)
                        """, (project_id, field_name))
                        self.connection.commit()
                        cursor.execute("SELECT LAST_INSERT_ID()")
                        if project_name not in field_ids:
                            field_ids[project_name] = {}
                        field_ids[project_name][field_name] = cursor.fetchone()[0]
                    else:
                        if project_name not in field_ids:
                            field_ids[project_name] = {}
                        field_ids[project_name][field_name] = result[0]

            # Add posts - making sure to verify user existence first
            post_data = [
                (1, "JohnDoe", "Just voted! The lines were long but it's our civic duty. #Election2023",
                 "2023-05-12 10:30:00", "Dallas", "TX", "USA", 120, 5, False),
                (2, "JaneSmith", "Trying out the new iPhone - amazing camera quality! #tech #Apple",
                 "2023-06-03 15:45:00", "Austin", "TX", "USA", 250, 3, True),
                (1, "TechGuru", "AI is advancing faster than regulations can keep up. We need thoughtful policies now.",
                 "2023-05-20 09:15:00", "San Francisco", "CA", "USA", 430, 12, False),
                (3, "FitnessFan", "My 30-day fitness challenge is complete! Before and after pics attached. #fitness",
                 "2023-06-10 18:00:00", "Miami", "FL", "USA", 380, 2, True),
                (2, "Traveler123", "Amazing sunset at the Grand Canyon! Nature at its best. #travel",
                 "2023-07-05 20:10:00", "Grand Canyon", "AZ", "USA", 520, 1, True),
                (3, "FoodLover", "Made homemade pasta for the first time. Recipe in comments! #foodie",
                 "2023-06-22 19:30:00", "Chicago", "IL", "USA", 190, 0, True),
                (1, "GamerPro", "New game release day! Can't wait to start playing. #gaming",
                 "2023-07-15 12:00:00", "Seattle", "WA", "USA", 150, 4, False),
                (2, "ArtCreator", "My latest painting inspired by climate change. Thoughts? #art",
                 "2023-06-28 14:20:00", "New York", "NY", "USA", 310, 2, True),
                (3, "SportsEnthusiast", "What a game! Can't believe that last-minute goal. #soccer",
                 "2023-07-10 22:45:00", "Boston", "MA", "USA", 280, 8, False),
                (1, "MusicFan", "This new album is fire! Been on repeat all day. #music",
                 "2023-06-15 16:35:00", "Nashville", "TN", "USA", 210, 3, False),
                (2, "JohnDoe", "Climate change is real. Here's what we can all do to help. #environment",
                 "2023-07-12 11:25:00", "Portland", "OR", "USA", 420, 15, True),
                (3, "JaneSmith", "Volunteering at the animal shelter today. These pets need homes! #adoption",
                 "2023-07-18 13:40:00", "San Diego", "CA", "USA", 350, 0, True),
                (1, "TechGuru", "5G rollout is happening faster than expected. Great for IoT applications.",
                 "2023-06-25 10:05:00", "Denver", "CO", "USA", 290, 6, False),
                (2, "FitnessFan", "Nutrition is 80% of your fitness journey. Focus on whole foods. #health",
                 "2023-07-20 07:30:00", "Phoenix", "AZ", "USA", 270, 2, False),
                (3, "Traveler123", "Local markets are the best way to experience a culture. #travel #food",
                 "2023-06-19 12:15:00", "Philadelphia", "PA", "USA", 330, 1, True)
            ]

            post_ids = {}
            for sm_id, username, text, time_posted, city, state, country, likes, dislikes, has_multimedia in post_data:
                # First verify the user exists
                cursor.execute("SELECT ID FROM User WHERE SM_ID = %s AND Username = %s", (sm_id, username))
                if not cursor.fetchone():
                    messagebox.showinfo("Info",
                                        f"Skipping post for user {username} on platform {sm_id} - user doesn't exist")
                    continue

                cursor.execute("""
                    SELECT ID FROM Post 
                    WHERE SM_ID = %s AND Username = %s AND Time_Posted = %s
                """, (sm_id, username, time_posted))

                result = cursor.fetchone()
                if not result:
                    cursor.execute("""
                        INSERT INTO Post (SM_ID, Username, Text_Post, Time_Posted, City_of_Post, 
                        State_of_Post, Country_of_Post, Likes, Dislikes, Has_Multimedia)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (sm_id, username, text, time_posted, city, state, country,
                          likes, dislikes, has_multimedia))
                    self.connection.commit()
                    cursor.execute("SELECT LAST_INSERT_ID()")
                    post_ids[(username, time_posted)] = cursor.fetchone()[0]
                else:
                    post_ids[(username, time_posted)] = result[0]

            # Associate posts with projects and add analysis results
            associations = [
                # Political Sentiment Analysis project
                ("JohnDoe", "2023-05-12 10:30:00", "Political Sentiment Analysis", {
                    "Sentiment": "Positive",
                    "Political_Leaning": "Neutral",
                    "Topic": "Voting",
                    "Region": "Southwest"
                }),
                ("TechGuru", "2023-05-20 09:15:00", "Political Sentiment Analysis", {
                    "Sentiment": "Concerned",
                    "Political_Leaning": "Moderate",
                    "Topic": "Technology Regulation",
                    "Region": "West"
                }),
                ("JohnDoe", "2023-07-12 11:25:00", "Political Sentiment Analysis", {
                    "Sentiment": "Urgent",
                    "Political_Leaning": "Progressive",
                    "Topic": "Environment",
                    "Region": "Northwest"
                }),

                # Brand Engagement Study
                ("JaneSmith", "2023-06-03 15:45:00", "Brand Engagement Study", {
                    "Sentiment": "Positive",
                    "Brand_Mentioned": "Apple",
                    "Engagement_Level": "High",
                    "Demographics": "Tech-savvy"
                }),
                ("GamerPro", "2023-07-15 12:00:00", "Brand Engagement Study", {
                    "Sentiment": "Excited",
                    "Brand_Mentioned": "Gaming",
                    "Engagement_Level": "Medium",
                    "Demographics": "Young Adult"
                }),
                ("MusicFan", "2023-06-15 16:35:00", "Brand Engagement Study", {
                    "Sentiment": "Positive",
                    "Brand_Mentioned": "Music",
                    "Engagement_Level": "High",
                    "Demographics": "Young Adult"
                }),

                # COVID-19 Information Spread
                ("TechGuru", "2023-06-25 10:05:00", "COVID-19 Information Spread", {
                    "Information_Type": "Technology",
                    "Accuracy": "Factual",
                    "Source_Cited": "No",
                    "Reach": "Medium"
                }),
                ("FitnessFan", "2023-07-20 07:30:00", "COVID-19 Information Spread", {
                    "Information_Type": "Health",
                    "Accuracy": "Factual",
                    "Source_Cited": "No",
                    "Reach": "Medium"
                }),
                ("JaneSmith", "2023-07-18 13:40:00", "COVID-19 Information Spread", {
                    "Information_Type": "Community",
                    "Accuracy": "Factual",
                    "Source_Cited": "No",
                    "Reach": "Low"
                }),

                # Environmental Awareness Campaign
                ("JohnDoe", "2023-07-12 11:25:00", "Environmental Awareness Campaign", {
                    "Environmental_Issue": "Climate Change",
                    "Call_To_Action": "Personal Actions",
                    "Target_Audience": "General Public",
                    "Geographic_Focus": "Global"
                }),
                ("ArtCreator", "2023-06-28 14:20:00", "Environmental Awareness Campaign", {
                    "Environmental_Issue": "Climate Change",
                    "Call_To_Action": "Awareness",
                    "Target_Audience": "Art Community",
                    "Geographic_Focus": "Urban"
                }),
                ("Traveler123", "2023-07-05 20:10:00", "Environmental Awareness Campaign", {
                    "Environmental_Issue": "Conservation",
                    "Call_To_Action": "Appreciation",
                    "Target_Audience": "Travelers",
                    "Geographic_Focus": "National Parks"
                })
            ]

            for username, time_posted, project_name, field_values in associations:
                if (username, time_posted) not in post_ids:
                    messagebox.showinfo("Info",
                                        f"Skipping association for post by {username} at {time_posted} - post doesn't exist")
                    continue

                post_id = post_ids.get((username, time_posted))
                project_id = project_ids.get(project_name)

                if post_id and project_id:
                    # First, associate the post with the project using PostAssociation field
                    assoc_field_id = field_ids[project_name]["PostAssociation"]

                    cursor.execute("""
                        SELECT ID FROM AnalysisResults 
                        WHERE Project_ID = %s AND Post_ID = %s AND Field_ID = %s
                    """, (project_id, post_id, assoc_field_id))

                    if not cursor.fetchone():
                        cursor.execute("""
                            INSERT INTO AnalysisResults (Project_ID, Post_ID, Field_ID, Field_Value)
                            VALUES (%s, %s, %s, 'Associated')
                        """, (project_id, post_id, assoc_field_id))
                        self.connection.commit()

                    # Then add the analysis results
                    for field_name, field_value in field_values.items():
                        if field_name in field_ids[project_name]:
                            field_id = field_ids[project_name][field_name]

                            cursor.execute("""
                                SELECT ID FROM AnalysisResults 
                                WHERE Project_ID = %s AND Post_ID = %s AND Field_ID = %s
                            """, (project_id, post_id, field_id))

                            if not cursor.fetchone():
                                cursor.execute("""
                                    INSERT INTO AnalysisResults (Project_ID, Post_ID, Field_ID, Field_Value)
                                    VALUES (%s, %s, %s, %s)
                                """, (project_id, post_id, field_id, field_value))
                                self.connection.commit()

            # Final commit
            self.connection.commit()
            messagebox.showinfo("Success", "Sample dataset has been added to the database")

            # Refresh dropdowns
            self.populate_project_dropdown()

        except mysql.connector.Error as err:
            self.connection.rollback()
            messagebox.showerror("Database Error", f"Failed to populate data: {err}")
    def populate_project_dropdown(self):
        if self.connection:
            try:
                cursor = self.connection.cursor()
                cursor.execute("SELECT Name FROM Project ORDER BY Name")
                projects = [row[0] for row in cursor.fetchall()]
                if projects:
                    self.project_dropdown['values'] = projects
                    self.analysis_project['values'] = projects
                    self.combined_project['values'] = projects
                    self.project_field_dropdown['values'] = projects
                cursor.close()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error loading projects: {err}")
    def save_project(self):
        proj_name = self.project_name.get()
        manager_first = self.manager_fname.get()
        manager_last = self.manager_lname.get()
        inst_name = self.institution.get()
        start = self.start_date.get()
        end = self.end_date.get()

        if not all([proj_name, manager_first, manager_last, inst_name, start, end]):
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            cursor = self.connection.cursor()

            # Check if institution exists, create if not
            cursor.execute("SELECT Name FROM Institution WHERE Name = %s", (inst_name,))
            if not cursor.fetchone():
                cursor.execute("INSERT INTO Institution (Name) VALUES (%s)", (inst_name,))

            # Insert project
            cursor.execute("""
                INSERT INTO Project (Name, PM_First_Name, PM_Last_Name, Institution_Name, Start_Date, End_Date)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (proj_name, manager_first, manager_last, inst_name, start, end))

            self.connection.commit()
            messagebox.showinfo("Success", "Project saved successfully")

            # Clear form fields
            self.project_name.delete(0, tk.END)
            self.manager_fname.delete(0, tk.END)
            self.manager_lname.delete(0, tk.END)
            self.institution.delete(0, tk.END)
            self.start_date.delete(0, tk.END)
            self.end_date.delete(0, tk.END)

            # Refresh dropdowns
            self.populate_project_dropdown()
        except mysql.connector.Error as err:
            self.connection.rollback()
            messagebox.showerror("Database Error", f"Failed to save project: {err}")
    def add_project_field(self):
        proj = self.project_field_dropdown.get()
        field_name = self.new_field_name.get()

        if not all([proj, field_name]):
            messagebox.showerror("Error", "Project and field name are required")
            return

        try:
            cursor = self.connection.cursor()

            # Get project ID
            cursor.execute("SELECT ID FROM Project WHERE Name = %s", (proj,))
            project_result = cursor.fetchone()

            if not project_result:
                messagebox.showerror("Error", "Project not found")
                return

            project_id = project_result[0]

            # Check if field already exists
            cursor.execute("""
                SELECT ID FROM ProjectFields 
                WHERE Project_ID = %s AND Field_Name = %s
            """, (project_id, field_name))

            if cursor.fetchone():
                messagebox.showinfo("Info", "Field already exists for this project")
                return

            # Add new field
            cursor.execute("""
                INSERT INTO ProjectFields (Project_ID, Field_Name)
                VALUES (%s, %s)
            """, (project_id, field_name))

            self.connection.commit()
            messagebox.showinfo("Success", "Field added to project")
            self.new_field_name.delete(0, tk.END)

            # Refresh field list
            self.load_project_fields()
        except mysql.connector.Error as err:
            self.connection.rollback()
            messagebox.showerror("Database Error", f"Failed to add field: {err}")
    def load_project_fields(self, event=None):
        proj = self.project_field_dropdown.get()

        if not proj:
            return

        try:
            # Clear existing items
            for item in self.fields_tree.get_children():
                self.fields_tree.delete(item)

            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT Field_Name FROM ProjectFields
                JOIN Project ON ProjectFields.Project_ID = Project.ID
                WHERE Project.Name = %s
            """, (proj,))

            for idx, row in enumerate(cursor.fetchall()):
                self.fields_tree.insert("", "end", values=(proj, row[0]))

            cursor.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error loading fields: {err}")
    def save_post(self):
        proj = self.project_dropdown.get()
        sm = self.social_media.get()
        user = self.username.get()
        text = self.post_text.get("1.0", tk.END).strip()
        p_time = self.post_time.get()

        if not all([proj, sm, user, text, p_time]):
            messagebox.showerror("Error", "Project, Social Media, Username, Text, and Time are required")
            return

        try:
            cursor = self.connection.cursor()

            # Handle Social Media
            cursor.execute("SELECT ID FROM SocialMedia WHERE Name = %s", (sm,))
            sm_result = cursor.fetchone()

            if not sm_result:
                cursor.execute("INSERT INTO SocialMedia (Name) VALUES (%s)", (sm,))
                self.connection.commit()
                cursor.execute("SELECT ID FROM SocialMedia WHERE Name = %s", (sm,))
                sm_result = cursor.fetchone()

            sm_id = sm_result[0]

            # Handle User
            cursor.execute("SELECT ID FROM User WHERE SM_ID = %s AND Username = %s", (sm_id, user))
            user_result = cursor.fetchone()

            if not user_result:
                cursor.execute("""
                    INSERT INTO User (SM_ID, Username, First_Name, Last_Name, 
                                   Country_of_Birth, Country_of_Residence, Age, Gender, Is_Verified)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    sm_id, user,
                    self.user_fname.get() or None,
                    self.user_lname.get() or None,
                    self.birth_country.get() or None,
                    self.residence_country.get() or None,
                    self.age.get() or None,
                    self.gender.get() or None,
                    self.verified_var.get()
                ))
                self.connection.commit()

            # Check if post already exists
            cursor.execute("""
                SELECT ID FROM Post 
                WHERE SM_ID = %s AND Username = %s AND Time_Posted = %s
            """, (sm_id, user, p_time))

            post_result = cursor.fetchone()

            if post_result:
                post_id = post_result[0]
                messagebox.showinfo("Info", "Post already exists - associating with project")
            else:
                # Create new post
                cursor.execute("""
                    INSERT INTO Post (
                        SM_ID, Username, Text_Post, Time_Posted,
                        City_of_Post, State_of_Post, Country_of_Post,
                        Likes, Dislikes, Has_Multimedia
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    sm_id, user, text, p_time,
                    self.city.get() or None,
                    self.state.get() or None,
                    self.country.get() or None,
                    self.likes.get() or 0,
                    self.dislikes.get() or 0,
                    self.multimedia_var.get()
                ))

                self.connection.commit()
                cursor.execute("SELECT LAST_INSERT_ID()")
                post_id = cursor.fetchone()[0]

            # Associate post with project (without creating a field)
            cursor.execute("SELECT ID FROM Project WHERE Name = %s", (proj,))
            project_id = cursor.fetchone()[0]

            # Instead of creating a field, we'll create a direct association
            # For this, we need a new table PostProjects or modify how we use AnalysisResults
            # Here, we'll directly insert into AnalysisResults with a special field ID

            # Get or create a system field for tracking posts
            cursor.execute("""
                SELECT ID FROM ProjectFields 
                WHERE Project_ID = %s AND Field_Name = 'PostAssociation'
            """, (project_id,))

            field_result = cursor.fetchone()
            if not field_result:
                cursor.execute("""
                    INSERT INTO ProjectFields (Project_ID, Field_Name)
                    VALUES (%s, 'PostAssociation')
                """, (project_id,))
                self.connection.commit()

                cursor.execute("""
                    SELECT ID FROM ProjectFields 
                    WHERE Project_ID = %s AND Field_Name = 'PostAssociation'
                """, (project_id,))
                field_result = cursor.fetchone()

            field_id = field_result[0]

            # Associate post with project
            cursor.execute("""
                SELECT ID FROM AnalysisResults
                WHERE Project_ID = %s AND Post_ID = %s AND Field_ID = %s
            """, (project_id, post_id, field_id))

            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO AnalysisResults (Project_ID, Post_ID, Field_ID, Field_Value)
                    VALUES (%s, %s, %s, 'Associated')
                """, (project_id, post_id, field_id))

            self.connection.commit()
            messagebox.showinfo("Success", "Post associated with project")

            # Clear form fields
            self.username.delete(0, tk.END)
            self.post_text.delete("1.0", tk.END)
            self.post_time.delete(0, tk.END)
            self.city.delete(0, tk.END)
            self.state.delete(0, tk.END)
            self.country.delete(0, tk.END)
            self.likes.delete(0, tk.END)
            self.dislikes.delete(0, tk.END)
            self.multimedia_var.set(False)

        except mysql.connector.Error as err:
            self.connection.rollback()
            messagebox.showerror("Database Error", f"Error: {err}")
    def populate_fields_dropdown(self, event=None):
        if self.connection:
            proj = self.analysis_project.get()

            if not proj:
                return

            try:
                cursor = self.connection.cursor()
                cursor.execute("""
                    SELECT Field_Name FROM ProjectFields
                    JOIN Project ON ProjectFields.Project_ID = Project.ID
                    WHERE Project.Name = %s AND Field_Name != 'PostAssociation'
                """, (proj,))

                fields = [row[0] for row in cursor.fetchall()]

                if fields:
                    self.field_dropdown['values'] = fields

                cursor.close()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error loading fields: {err}")
    def save_analysis(self):
        proj = self.analysis_project.get()
        field = self.field_dropdown.get()
        post_id_val = self.post_id.get()
        value = self.field_value.get()

        if not all([proj, field, post_id_val, value]):
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            cursor = self.connection.cursor()

            # Get project ID
            cursor.execute("SELECT ID FROM Project WHERE Name = %s", (proj,))
            project_id = cursor.fetchone()[0]

            # Get field ID
            cursor.execute("""
                SELECT ID FROM ProjectFields 
                WHERE Project_ID = %s AND Field_Name = %s
            """, (project_id, field))

            field_result = cursor.fetchone()

            if not field_result:
                messagebox.showerror("Error", "Field not found for this project")
                return

            field_id = field_result[0]

            # Check if analysis result already exists
            cursor.execute("""
                SELECT ID FROM AnalysisResults 
                WHERE Project_ID = %s AND Post_ID = %s AND Field_ID = %s
            """, (project_id, post_id_val, field_id))

            result = cursor.fetchone()

            if result:
                # Update existing result
                cursor.execute("""
                    UPDATE AnalysisResults 
                    SET Field_Value = %s 
                    WHERE ID = %s
                """, (value, result[0]))
            else:
                # Insert new result
                cursor.execute("""
                    INSERT INTO AnalysisResults (Project_ID, Post_ID, Field_ID, Field_Value) 
                    VALUES (%s, %s, %s, %s)
                """, (project_id, post_id_val, field_id, value))

            self.connection.commit()
            messagebox.showinfo("Success", "Analysis result saved")
            self.field_value.delete(0, tk.END)

        except mysql.connector.Error as err:
            self.connection.rollback()
            messagebox.showerror("Database Error", f"Error: {err}")
    def reset_project_data(self):
        """Reset only project-related data"""
        if messagebox.askyesno("Warning",
                               "This will delete ALL project data including analysis results. Are you sure?"):
            try:
                cursor = self.connection.cursor()

                # Disable foreign key checks temporarily
                cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

                # Truncate tables in reverse order of dependencies
                cursor.execute("TRUNCATE TABLE AnalysisResults")
                cursor.execute("TRUNCATE TABLE ProjectFields")
                cursor.execute("TRUNCATE TABLE Project")

                # Enable foreign key checks again
                cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

                self.connection.commit()
                messagebox.showinfo("Success", "All project data has been cleared")

                # Refresh the project dropdowns
                self.populate_project_dropdown()

                # Clear any project fields in the tree view
                for item in self.fields_tree.get_children():
                    self.fields_tree.delete(item)

            except mysql.connector.Error as err:
                self.connection.rollback()
                messagebox.showerror("Database Error", f"Failed to clear project data: {err}")
    def reset_all_data(self):
        """Reset the entire database"""
        if messagebox.askyesno("WARNING",
                               "This will delete ALL DATA in the database, including posts, users, and social media. This cannot be undone. Are you sure?"):
            try:
                cursor = self.connection.cursor()

                # Disable foreign key checks temporarily
                cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

                # Truncate all tables in reverse order of dependencies
                cursor.execute("TRUNCATE TABLE AnalysisResults")
                cursor.execute("TRUNCATE TABLE ProjectFields")
                cursor.execute("TRUNCATE TABLE Project")
                cursor.execute("TRUNCATE TABLE Post")
                cursor.execute("TRUNCATE TABLE User")
                cursor.execute("TRUNCATE TABLE SocialMedia")
                cursor.execute("TRUNCATE TABLE Institution")

                # Enable foreign key checks again
                cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

                self.connection.commit()
                messagebox.showinfo("Success", "All data has been cleared from the database")

                # Refresh all dropdowns
                self.populate_project_dropdown()

            except mysql.connector.Error as err:
                self.connection.rollback()
                messagebox.showerror("Database Error", f"Failed to clear database: {err}")
    def query_by_social_media(self):
        sm = self.query_sm.get()

        if not sm:
            messagebox.showerror("Error", "Please select a social media platform")
            return

        try:
            cursor = self.connection.cursor()

            query = """
                SELECT 
                    p.ID as Post_ID,
                    p.Text_Post,
                    sm.Name as Social_Media,
                    p.Username,
                    p.Time_Posted,
                    GROUP_CONCAT(DISTINCT pr.Name ORDER BY pr.Name SEPARATOR ', ') AS Experiment_Names
                FROM Post p
                JOIN SocialMedia sm ON p.SM_ID = sm.ID
                LEFT JOIN AnalysisResults ar ON p.ID = ar.Post_ID
                LEFT JOIN Project pr ON ar.Project_ID = pr.ID
                WHERE sm.Name = %s
                GROUP BY p.ID, p.Text_Post, sm.Name, p.Username, p.Time_Posted
                ORDER BY sm.Name ASC, p.Time_Posted DESC
            """

            cursor.execute(query, (sm,))
            results = cursor.fetchall()
            self.display_query_results(results)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
    def query_by_date_range(self):
        start_date = self.query_start_date.get()
        end_date = self.query_end_date.get()

        if not all([start_date, end_date]):
            messagebox.showerror("Error", "Please enter both start and end dates")
            return

        try:
            # Validate dates
            try:
                start = datetime.strptime(start_date, '%Y-%m-%d').date()
                end = datetime.strptime(end_date, '%Y-%m-%d').date()
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD")
                return

            if start > end:
                messagebox.showerror("Error", "Start date cannot be later than end date")
                return

            cursor = self.connection.cursor()

            query = """
                SELECT 
                    p.ID as Post_ID,
                    p.Text_Post,
                    sm.Name as Social_Media,
                    p.Username,
                    p.Time_Posted,
                    GROUP_CONCAT(DISTINCT pr.Name ORDER BY pr.Name SEPARATOR ', ') AS Experiment_Names
                FROM Post p
                JOIN SocialMedia sm ON p.SM_ID = sm.ID
                LEFT JOIN AnalysisResults ar ON p.ID = ar.Post_ID
                LEFT JOIN Project pr ON ar.Project_ID = pr.ID
                WHERE p.Time_Posted BETWEEN %s AND %s
                GROUP BY p.ID, p.Text_Post, sm.Name, p.Username, p.Time_Posted
                ORDER BY sm.Name ASC, p.Time_Posted DESC
            """

            cursor.execute(query, (start_date, end_date))
            results = cursor.fetchall()
            self.display_query_results(results)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
    def query_by_user(self):
        sm = self.user_query_sm.get()
        username = self.user_query_name.get()

        if not all([sm, username]):
            messagebox.showerror("Error", "Please select a social media platform and enter a username")
            return

        try:
            cursor = self.connection.cursor()

            query = """
                SELECT 
                    p.ID as Post_ID,
                    p.Text_Post,
                    sm.Name as Social_Media,
                    p.Username,
                    p.Time_Posted,
                    GROUP_CONCAT(DISTINCT pr.Name ORDER BY pr.Name SEPARATOR ', ') AS Experiment_Names
                FROM Post p
                JOIN SocialMedia sm ON p.SM_ID = sm.ID
                LEFT JOIN AnalysisResults ar ON p.ID = ar.Post_ID
                LEFT JOIN Project pr ON ar.Project_ID = pr.ID
                WHERE sm.Name = %s AND p.Username = %s
                GROUP BY p.ID, p.Text_Post, sm.Name, p.Username, p.Time_Posted
                ORDER BY sm.Name ASC, p.Time_Posted DESC
            """

            cursor.execute(query, (sm, username))
            results = cursor.fetchall()
            self.display_query_results(results)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
    def query_by_full_name(self):
        first_name = self.first_name_query.get()
        last_name = self.last_name_query.get()

        if not all([first_name, last_name]):
            messagebox.showerror("Error", "Please enter both first and last name")
            return

        try:
            cursor = self.connection.cursor()

            query = """
                SELECT 
                    p.ID as Post_ID,
                    p.Text_Post,
                    sm.Name as Social_Media,
                    p.Username,
                    p.Time_Posted,
                    GROUP_CONCAT(DISTINCT pr.Name ORDER BY pr.Name SEPARATOR ', ') AS Experiment_Names
                FROM Post p
                JOIN SocialMedia sm ON p.SM_ID = sm.ID
                JOIN User u ON p.Username = u.Username AND p.SM_ID = u.SM_ID
                LEFT JOIN AnalysisResults ar ON p.ID = ar.Post_ID
                LEFT JOIN Project pr ON ar.Project_ID = pr.ID
                WHERE u.First_Name = %s AND u.Last_Name = %s
                GROUP BY p.ID, p.Text_Post, sm.Name, p.Username, p.Time_Posted
                ORDER BY sm.Name ASC, p.Time_Posted DESC
            """

            cursor.execute(query, (first_name, last_name))
            results = cursor.fetchall()
            self.display_query_results(results)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
    def query_by_multimedia(self):
        has_multimedia = self.mm_var.get()

        try:
            cursor = self.connection.cursor()

            query = """
                SELECT 
                    p.ID as Post_ID,
                    p.Text_Post,
                    sm.Name as Social_Media,
                    p.Username,
                    p.Time_Posted,
                    GROUP_CONCAT(DISTINCT pr.Name ORDER BY pr.Name SEPARATOR ', ') AS Experiment_Names
                FROM Post p
                JOIN SocialMedia sm ON p.SM_ID = sm.ID
                LEFT JOIN AnalysisResults ar ON p.ID = ar.Post_ID
                LEFT JOIN Project pr ON ar.Project_ID = pr.ID
                WHERE p.Has_Multimedia = %s
                GROUP BY p.ID, p.Text_Post, sm.Name, p.Username, p.Time_Posted
                ORDER BY sm.Name ASC, p.Time_Posted DESC
            """

            cursor.execute(query, (has_multimedia,))
            results = cursor.fetchall()
            self.display_query_results(results)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
    def query_experiment(self):
        exp_name = self.exp_name_entry.get()

        if not exp_name:
            messagebox.showerror("Error", "Please enter an experiment name")
            return

        try:
            cursor = self.connection.cursor()

            query = """
                WITH exp_fields AS (
                    SELECT 
                        ar1.Post_ID,
                        ar1.Field_ID,
                        ar1.Field_Value,
                        fcounts.field_count,
                        vcounts.value_count
                    FROM AnalysisResults ar1
                    JOIN Project p ON ar1.Project_ID = p.ID,
                    (SELECT Post_ID, Field_ID, COUNT(1) as field_count 
                     FROM AnalysisResults
                     GROUP BY Post_ID, Field_ID) fcounts,
                    (SELECT Post_ID, Field_ID, Field_Value, COUNT(1) as value_count
                     FROM AnalysisResults
                     GROUP BY Post_ID, Field_ID, Field_Value) vcounts
                    WHERE ar1.Post_ID = fcounts.Post_ID
                    AND ar1.Field_ID = fcounts.Field_ID
                    AND ar1.Field_ID = vcounts.Field_ID
                    AND ar1.Post_ID = vcounts.Post_ID
                    AND ar1.Field_Value = vcounts.Field_Value
                    AND p.Name = %s
                    ORDER BY Field_ID
                )
                SELECT 
                    Field_ID, 
                    Field_Value,
                    p.Text_Post, 
                    ROUND(SUM(value_count) / SUM(field_count), 2) as pct
                FROM exp_fields
                JOIN Post p ON exp_fields.Post_ID = p.ID
                GROUP BY Field_ID, Field_Value, p.Text_Post
                ORDER BY Field_ID
            """

            cursor.execute(query, (exp_name,))
            results = cursor.fetchall()

            # Clear existing results
            for item in self.exp_results_tree.get_children():
                self.exp_results_tree.delete(item)

            # Populate results
            for row in results:
                self.exp_results_tree.insert("", "end", values=(
                    row[0],  # Field_ID
                    row[1],  # Field_Value
                    row[2],  # Text_Post
                    row[3]  # pct
                ))

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
    def query_posts_then_experiments(self):
        # Get posts for the selected project
        posts = self.get_posts_by_criteria()

        if not posts:
            return

        post_ids = [str(p[0]) for p in posts]
        placeholder = ','.join(post_ids)

        try:
            cursor = self.connection.cursor()

            # Find experiments associated with these posts
            sql = f"""
                SELECT DISTINCT p.Name
                FROM Project p
                JOIN AnalysisResults ar ON p.ID = ar.Project_ID
                WHERE ar.Post_ID IN ({placeholder})
                ORDER BY p.Name
            """

            cursor.execute(sql)
            experiments = [r[0] for r in cursor.fetchall()]

            if not experiments:
                messagebox.showinfo("Notice", "None of these posts have been analyzed by any project.")
                return

            # Create a new window to display results
            dlg = tk.Toplevel(self.root)
            dlg.title("Experiments for Selected Posts")

            tree = ttk.Treeview(dlg, columns=("FieldID", "Value", "PostText", "Pct"), show="headings")
            for col, w in [("FieldID", 80), ("Value", 200), ("PostText", 300), ("Pct", 80)]:
                tree.heading(col, text=col)
                tree.column(col, width=w)

            tree.pack(fill="both", expand=True)

            # For each experiment, get the analysis results
            for name in experiments:
                tree.insert("", "end", values=(f"Experiment: {name}", "", "", ""))

                cur2 = self.connection.cursor()

                # Use the same query as query_experiment but modified to filter by post IDs
                query = f"""
                    WITH exp_fields AS (
                        SELECT 
                            ar1.Post_ID,
                            ar1.Field_ID,
                            ar1.Field_Value,
                            fcounts.field_count,
                            vcounts.value_count
                        FROM AnalysisResults ar1
                        JOIN Project p ON ar1.Project_ID = p.ID,
                        (SELECT Post_ID, Field_ID, COUNT(1) as field_count 
                         FROM AnalysisResults
                         GROUP BY Post_ID, Field_ID) fcounts,
                        (SELECT Post_ID, Field_ID, Field_Value, COUNT(1) as value_count
                         FROM AnalysisResults
                         GROUP BY Post_ID, Field_ID, Field_Value) vcounts
                        WHERE ar1.Post_ID = fcounts.Post_ID
                        AND ar1.Field_ID = fcounts.Field_ID
                        AND ar1.Field_ID = vcounts.Field_ID
                        AND ar1.Post_ID = vcounts.Post_ID
                        AND ar1.Field_Value = vcounts.Field_Value
                        AND p.Name = %s
                        AND ar1.Post_ID IN ({placeholder})
                        ORDER BY Field_ID
                    )
                    SELECT 
                        Field_ID, 
                        Field_Value,
                        p.Text_Post, 
                        ROUND(SUM(value_count) / SUM(field_count), 2) as pct
                    FROM exp_fields
                    JOIN Post p ON exp_fields.Post_ID = p.ID
                    GROUP BY Field_ID, Field_Value, p.Text_Post
                    ORDER BY Field_ID
                """

                cur2.execute(query, (name,))

                for row in cur2.fetchall():
                    tree.insert("", "end", values=(row[0], row[1], row[2], row[3]))

                cur2.close()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
    def get_posts_by_criteria(self):
        project_name = self.combined_project.get().strip()

        if not project_name:
            messagebox.showinfo("Notice", "Please select a project first.")
            return []

        sql = """
            SELECT 
                p.ID, 
                p.Text_Post, 
                sm.Name AS media, 
                p.Username, 
                p.Time_Posted
            FROM Post p
            JOIN SocialMedia sm ON p.SM_ID = sm.ID
            JOIN AnalysisResults ar ON p.ID = ar.Post_ID
            JOIN ProjectFields pf ON ar.Field_ID = pf.ID
            JOIN Project pr ON pf.Project_ID = pr.ID
            WHERE pr.Name = %s
            AND pf.Field_Name = 'PostAssociation'
            ORDER BY p.Time_Posted
        """

        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, (project_name,))
            posts = cursor.fetchall()

            # Display posts in the results tree
            for item in self.combined_results_tree.get_children():
                self.combined_results_tree.delete(item)

            for post in posts:
                self.combined_results_tree.insert("", "end", values=(
                    post[0],  # ID
                    post[1],  # Text_Post
                    post[2],  # media
                    post[3],  # Username
                    post[4]  # Time_Posted
                ))

            return posts
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to fetch posts: {err}")
            return []
    def display_query_results(self, results):
        # Clear existing results
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)

        # Populate with new results
        for row in results:
            exp_names = row[5] or 'No experiments associated'

            self.results_tree.insert("", "end", values=(
                row[0],  # Post_ID
                row[1],  # Text_Post
                row[2],  # Social_Media
                row[3],  # Username
                row[4],  # Time_Posted
                exp_names
            ))
# MAIN
if __name__ == "__main__":
    root = tk.Tk()
    app = SocialMediaAnalysisApp(root)
    root.mainloop()