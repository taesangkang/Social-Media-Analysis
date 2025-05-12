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

        # Create tabs in logical workflow order
        self.create_project_tab()
        self.create_fields_tab()
        self.create_posts_management_tab()
        self.create_association_tab()  # Renamed from create_posts_tab
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
    def create_posts_management_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Manage Posts")

        ttk.Label(tab, text="Create and Manage Posts", font=("Arial", 14)).grid(row=0, column=0, columnspan=4, pady=10,
                                                                                padx=10)

        # User Info Frame - Same as in associate_posts tab
        user_frame = ttk.LabelFrame(tab, text="User Information")
        user_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="nw")

        ttk.Label(user_frame, text="Social Media:").grid(row=0, column=0, pady=5, padx=5, sticky="e")
        self.post_social_media = ttk.Combobox(user_frame, width=25, values=["Facebook", "Twitter", "Instagram"])
        self.post_social_media.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(user_frame, text="Username:").grid(row=1, column=0, pady=5, padx=5, sticky="e")
        self.post_username = ttk.Entry(user_frame, width=25)
        self.post_username.grid(row=1, column=1, pady=5, padx=5)

        ttk.Label(user_frame, text="First Name:").grid(row=2, column=0, pady=5, padx=5, sticky="e")
        self.post_user_fname = ttk.Entry(user_frame, width=25)
        self.post_user_fname.grid(row=2, column=1, pady=5, padx=5)

        ttk.Label(user_frame, text="Last Name:").grid(row=3, column=0, pady=5, padx=5, sticky="e")
        self.post_user_lname = ttk.Entry(user_frame, width=25)
        self.post_user_lname.grid(row=3, column=1, pady=5, padx=5)

        ttk.Label(user_frame, text="Country of Birth:").grid(row=4, column=0, pady=5, padx=5, sticky="e")
        self.post_birth_country = ttk.Entry(user_frame, width=25)
        self.post_birth_country.grid(row=4, column=1, pady=5, padx=5)

        ttk.Label(user_frame, text="Country of Residence:").grid(row=5, column=0, pady=5, padx=5, sticky="e")
        self.post_residence_country = ttk.Entry(user_frame, width=25)
        self.post_residence_country.grid(row=5, column=1, pady=5, padx=5)

        ttk.Label(user_frame, text="Age:").grid(row=6, column=0, pady=5, padx=5, sticky="e")
        self.post_age = ttk.Entry(user_frame, width=25)
        self.post_age.grid(row=6, column=1, pady=5, padx=5)

        ttk.Label(user_frame, text="Gender:").grid(row=7, column=0, pady=5, padx=5, sticky="e")
        self.post_gender = ttk.Entry(user_frame, width=25)
        self.post_gender.grid(row=7, column=1, pady=5, padx=5)

        ttk.Label(user_frame, text="Verified User:").grid(row=8, column=0, pady=5, padx=5, sticky="e")
        self.post_verified_var = tk.BooleanVar()
        self.post_verified_check = ttk.Checkbutton(user_frame, variable=self.post_verified_var)
        self.post_verified_check.grid(row=8, column=1, pady=5, padx=5, sticky="w")

        # Post Info Frame - Same as in associate_posts tab
        post_frame = ttk.LabelFrame(tab, text="Post Information")
        post_frame.grid(row=1, column=2, columnspan=2, padx=10, pady=5, sticky="nw")

        ttk.Label(post_frame, text="Post Time (YYYY-MM-DD HH:MM):").grid(row=0, column=0, pady=5, padx=5, sticky="e")
        self.post_post_time = ttk.Entry(post_frame, width=25)
        self.post_post_time.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(post_frame, text="City:").grid(row=1, column=0, pady=5, padx=5, sticky="e")
        self.post_city = ttk.Entry(post_frame, width=25)
        self.post_city.grid(row=1, column=1, pady=5, padx=5)

        ttk.Label(post_frame, text="State:").grid(row=2, column=0, pady=5, padx=5, sticky="e")
        self.post_state = ttk.Entry(post_frame, width=25)
        self.post_state.grid(row=2, column=1, pady=5, padx=5)

        ttk.Label(post_frame, text="Country:").grid(row=3, column=0, pady=5, padx=5, sticky="e")
        self.post_country = ttk.Entry(post_frame, width=25)
        self.post_country.grid(row=3, column=1, pady=5, padx=5)

        ttk.Label(post_frame, text="Likes:").grid(row=4, column=0, pady=5, padx=5, sticky="e")
        self.post_likes = ttk.Entry(post_frame, width=25)
        self.post_likes.grid(row=4, column=1, pady=5, padx=5)

        ttk.Label(post_frame, text="Dislikes:").grid(row=5, column=0, pady=5, padx=5, sticky="e")
        self.post_dislikes = ttk.Entry(post_frame, width=25)
        self.post_dislikes.grid(row=5, column=1, pady=5, padx=5)

        ttk.Label(post_frame, text="Has Multimedia:").grid(row=6, column=0, pady=5, padx=5, sticky="e")
        self.post_multimedia_var = tk.BooleanVar()
        self.post_multimedia_check = ttk.Checkbutton(post_frame, variable=self.post_multimedia_var)
        self.post_multimedia_check.grid(row=6, column=1, pady=5, padx=5, sticky="w")

        # Post Text Frame - Same as in associate_posts tab
        post_text_frame = ttk.LabelFrame(tab, text="Post Text Content")
        post_text_frame.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

        self.post_post_text = tk.Text(post_text_frame, width=80, height=8)
        self.post_post_text.grid(row=0, column=0, pady=5, padx=5)

        text_scroll = ttk.Scrollbar(post_text_frame, orient="vertical", command=self.post_post_text.yview)
        text_scroll.grid(row=0, column=1, sticky="ns")
        self.post_post_text.configure(yscrollcommand=text_scroll.set)

        # Save button - but without project association
        self.save_post_only_button = ttk.Button(tab, text="Save Post", command=self.save_post_only)
        self.save_post_only_button.grid(row=3, column=0, columnspan=4, pady=20)

        # Add a section to view existing posts
        posts_list_frame = ttk.LabelFrame(tab, text="Existing Posts")
        posts_list_frame.grid(row=4, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        self.posts_tree = ttk.Treeview(posts_list_frame, columns=("ID", "Text", "Media", "User", "Time"),
                                       show="headings")

        # Set up columns and headings
        self.posts_tree.heading("ID", text="Post ID")
        self.posts_tree.heading("Text", text="Post Text")
        self.posts_tree.heading("Media", text="Social Media")
        self.posts_tree.heading("User", text="Username")
        self.posts_tree.heading("Time", text="Time Posted")

        self.posts_tree.column("ID", width=50)
        self.posts_tree.column("Text", width=300)
        self.posts_tree.column("Media", width=100)
        self.posts_tree.column("User", width=100)
        self.posts_tree.column("Time", width=150)

        # Add scrollbar for posts tree
        posts_scroll = ttk.Scrollbar(posts_list_frame, orient="vertical", command=self.posts_tree.yview)
        posts_scroll.pack(side="right", fill="y")
        self.posts_tree.configure(yscrollcommand=posts_scroll.set)
        self.posts_tree.pack(fill="both", expand=True, padx=5, pady=5)

        # Refresh button
        refresh_posts_button = ttk.Button(tab, text="Refresh Posts List", command=self.load_posts)
        refresh_posts_button.grid(row=5, column=0, columnspan=4, pady=10)

        # Configure row weights to make posts list expandable
        tab.grid_rowconfigure(4, weight=1)
    def create_association_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Associate Posts to Projects")

        ttk.Label(tab, text="Associate Existing Posts with Projects", font=("Arial", 14)).grid(row=0, column=0,
                                                                                               columnspan=4, pady=10,
                                                                                               padx=10)

        # Project selection
        project_frame = ttk.LabelFrame(tab, text="Select Project")
        project_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

        ttk.Label(project_frame, text="Project:").grid(row=0, column=0, pady=5, padx=5, sticky="e")
        self.project_dropdown = ttk.Combobox(project_frame, width=40)
        self.project_dropdown.grid(row=0, column=1, pady=5, padx=5)

        # When project is selected, show already associated posts
        self.project_dropdown.bind('<<ComboboxSelected>>', self.load_associated_posts)

        # Post selection section
        post_filter_frame = ttk.LabelFrame(tab, text="Find Posts to Associate")
        post_filter_frame.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

        # Search filters
        ttk.Label(post_filter_frame, text="Filter by Username:").grid(row=0, column=0, pady=5, padx=5)
        self.filter_username = ttk.Entry(post_filter_frame, width=20)
        self.filter_username.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(post_filter_frame, text="Filter by Social Media:").grid(row=0, column=2, pady=5, padx=5)
        self.filter_social_media = ttk.Combobox(post_filter_frame, width=15,
                                                values=["Facebook", "Twitter", "Instagram"])
        self.filter_social_media.grid(row=0, column=3, pady=5, padx=5)

        ttk.Label(post_filter_frame, text="Contains Text:").grid(row=1, column=0, pady=5, padx=5)
        self.filter_text = ttk.Entry(post_filter_frame, width=20)
        self.filter_text.grid(row=1, column=1, pady=5, padx=5)

        ttk.Label(post_filter_frame, text="Date Range:").grid(row=1, column=2, pady=5, padx=5)
        date_range_frame = ttk.Frame(post_filter_frame)
        date_range_frame.grid(row=1, column=3, pady=5, padx=5)

        self.filter_start_date = ttk.Entry(date_range_frame, width=10)
        self.filter_start_date.grid(row=0, column=0, padx=2)
        ttk.Label(date_range_frame, text="to").grid(row=0, column=1, padx=2)
        self.filter_end_date = ttk.Entry(date_range_frame, width=10)
        self.filter_end_date.grid(row=0, column=2, padx=2)

        filter_button = ttk.Button(post_filter_frame, text="Filter Posts", command=self.filter_posts_for_association)
        filter_button.grid(row=2, column=0, columnspan=4, pady=10)

        # Display available posts
        available_posts_frame = ttk.LabelFrame(tab, text="Available Posts")
        available_posts_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.available_posts_tree = ttk.Treeview(available_posts_frame,
                                                 columns=("ID", "Text", "Media", "User", "Time"),
                                                 show="headings",
                                                 selectmode="extended")

        self.available_posts_tree.heading("ID", text="Post ID")
        self.available_posts_tree.heading("Text", text="Post Text")
        self.available_posts_tree.heading("Media", text="Social Media")
        self.available_posts_tree.heading("User", text="Username")
        self.available_posts_tree.heading("Time", text="Time Posted")

        self.available_posts_tree.column("ID", width=50)
        self.available_posts_tree.column("Text", width=200)
        self.available_posts_tree.column("Media", width=80)
        self.available_posts_tree.column("User", width=80)
        self.available_posts_tree.column("Time", width=120)

        self.available_posts_tree.pack(fill="both", expand=True, padx=5, pady=5)

        # Display already associated posts
        associated_posts_frame = ttk.LabelFrame(tab, text="Posts Already Associated with Project")
        associated_posts_frame.grid(row=3, column=2, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.associated_posts_tree = ttk.Treeview(associated_posts_frame,
                                                  columns=("ID", "Text", "Media", "User", "Time"),
                                                  show="headings")

        self.associated_posts_tree.heading("ID", text="Post ID")
        self.associated_posts_tree.heading("Text", text="Post Text")
        self.associated_posts_tree.heading("Media", text="Social Media")
        self.associated_posts_tree.heading("User", text="Username")
        self.associated_posts_tree.heading("Time", text="Time Posted")

        self.associated_posts_tree.column("ID", width=50)
        self.associated_posts_tree.column("Text", width=200)
        self.associated_posts_tree.column("Media", width=80)
        self.associated_posts_tree.column("User", width=80)
        self.associated_posts_tree.column("Time", width=120)

        self.associated_posts_tree.pack(fill="both", expand=True, padx=5, pady=5)

        # Buttons for association
        button_frame = ttk.Frame(tab)
        button_frame.grid(row=4, column=0, columnspan=4, pady=10, padx=10)

        associate_button = ttk.Button(button_frame, text="Associate Selected Posts with Project →",
                                      command=self.associate_selected_posts)
        associate_button.grid(row=0, column=0, padx=10)

        remove_button = ttk.Button(button_frame, text="← Remove Posts from Project",
                                   command=self.remove_posts_from_project)
        remove_button.grid(row=0, column=1, padx=10)

        # Configure row weights to make post trees expandable
        tab.grid_rowconfigure(3, weight=1)
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_columnconfigure(1, weight=1)
        tab.grid_columnconfigure(2, weight=1)
        tab.grid_columnconfigure(3, weight=1)
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
    def filter_posts_for_association(self):
        """Find posts based on filter criteria"""
        if not self.project_dropdown.get():
            messagebox.showinfo("Notice", "Please select a project first")
            return

        try:
            cursor = self.connection.cursor()

            # Start with base query
            query = """
                SELECT 
                    p.ID as Post_ID,
                    p.Text_Post,
                    sm.Name as Social_Media,
                    p.Username,
                    p.Time_Posted
                FROM Post p
                JOIN SocialMedia sm ON p.SM_ID = sm.ID
                WHERE 1=1
            """
            params = []

            # Add filters based on what's filled in
            if self.filter_username.get():
                query += " AND p.Username LIKE %s"
                params.append(f"%{self.filter_username.get()}%")

            if self.filter_social_media.get():
                query += " AND sm.Name = %s"
                params.append(self.filter_social_media.get())

            if self.filter_text.get():
                query += " AND p.Text_Post LIKE %s"
                params.append(f"%{self.filter_text.get()}%")

            if self.filter_start_date.get() and self.filter_end_date.get():
                query += " AND p.Time_Posted BETWEEN %s AND %s"
                params.append(self.filter_start_date.get())
                params.append(self.filter_end_date.get())

            # Exclude posts already associated with this project
            project_id = self.get_project_id(self.project_dropdown.get())
            if project_id:
                query += """
                    AND p.ID NOT IN (
                        SELECT Post_ID FROM AnalysisResults 
                        WHERE Project_ID = %s AND Field_ID IN (
                            SELECT ID FROM ProjectFields 
                            WHERE Project_ID = %s AND Field_Name = 'PostAssociation'
                        )
                    )
                """
                params.append(project_id)
                params.append(project_id)

            query += " ORDER BY p.Time_Posted DESC"

            cursor.execute(query, params)
            results = cursor.fetchall()

            # Clear existing items
            for item in self.available_posts_tree.get_children():
                self.available_posts_tree.delete(item)

            # Populate tree with filtered posts
            for row in results:
                post_id = row[0]
                text = row[1]
                # Truncate text if too long for display
                if len(text) > 30:
                    text = text[:27] + "..."

                self.available_posts_tree.insert("", "end", values=(
                    post_id,
                    text,
                    row[2],  # Social_Media
                    row[3],  # Username
                    row[4]  # Time_Posted
                ))

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error filtering posts: {err}")
    def load_associated_posts(self, event=None):
        """Load posts already associated with the selected project"""
        project = self.project_dropdown.get()

        if not project:
            return

        try:
            cursor = self.connection.cursor()

            # Get project ID
            project_id = self.get_project_id(project)

            if not project_id:
                return

            # Find field ID for PostAssociation
            cursor.execute("""
                SELECT ID FROM ProjectFields 
                WHERE Project_ID = %s AND Field_Name = 'PostAssociation'
            """, (project_id,))

            field_result = cursor.fetchone()
            if not field_result:
                # No posts associated yet
                for item in self.associated_posts_tree.get_children():
                    self.associated_posts_tree.delete(item)
                return

            field_id = field_result[0]

            # Get associated posts
            query = """
                SELECT 
                    p.ID as Post_ID,
                    p.Text_Post,
                    sm.Name as Social_Media,
                    p.Username,
                    p.Time_Posted
                FROM Post p
                JOIN SocialMedia sm ON p.SM_ID = sm.ID
                JOIN AnalysisResults ar ON p.ID = ar.Post_ID
                WHERE ar.Project_ID = %s AND ar.Field_ID = %s
                ORDER BY p.Time_Posted DESC
            """

            cursor.execute(query, (project_id, field_id))
            results = cursor.fetchall()

            # Clear existing items
            for item in self.associated_posts_tree.get_children():
                self.associated_posts_tree.delete(item)

            # Populate tree with associated posts
            for row in results:
                post_id = row[0]
                text = row[1]
                # Truncate text if too long for display
                if len(text) > 30:
                    text = text[:27] + "..."

                self.associated_posts_tree.insert("", "end", values=(
                    post_id,
                    text,
                    row[2],  # Social_Media
                    row[3],  # Username
                    row[4]  # Time_Posted
                ))

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error loading associated posts: {err}")
    def get_project_id(self, project_name):
        """Helper to get project ID from name"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT ID FROM Project WHERE Name = %s", (project_name,))
            result = cursor.fetchone()
            if result:
                return result[0]
            return None
        except mysql.connector.Error:
            return None
    def associate_selected_posts(self):
        """Associate selected posts with the current project"""
        project = self.project_dropdown.get()

        if not project:
            messagebox.showerror("Error", "Please select a project")
            return

        # Get selected posts
        selected_items = self.available_posts_tree.selection()

        if not selected_items:
            messagebox.showinfo("Notice", "Please select at least one post to associate")
            return

        post_ids = [self.available_posts_tree.item(item, "values")[0] for item in selected_items]

        try:
            cursor = self.connection.cursor()

            # Get project ID
            project_id = self.get_project_id(project)

            if not project_id:
                messagebox.showerror("Error", "Project not found")
                return

            # Get or create the PostAssociation field
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

            # Associate each post
            associated_count = 0

            for post_id in post_ids:
                # Create new association
                cursor.execute("""
                    INSERT INTO AnalysisResults (Project_ID, Post_ID, Field_ID, Field_Value)
                    VALUES (%s, %s, %s, 'Associated')
                """, (project_id, post_id, field_id))

                associated_count += 1

            self.connection.commit()

            messagebox.showinfo("Success", f"Successfully associated {associated_count} posts with the project")

            # Refresh both trees
            self.load_associated_posts()
            self.filter_posts_for_association()

        except mysql.connector.Error as err:
            self.connection.rollback()
            messagebox.showerror("Database Error", f"Error associating posts: {err}")
    def remove_posts_from_project(self):
        """Remove selected posts from the current project"""
        project = self.project_dropdown.get()

        if not project:
            messagebox.showerror("Error", "Please select a project")
            return

        # Get selected posts
        selected_items = self.associated_posts_tree.selection()

        if not selected_items:
            messagebox.showinfo("Notice", "Please select at least one post to remove")
            return

        post_ids = [self.associated_posts_tree.item(item, "values")[0] for item in selected_items]

        if not messagebox.askyesno("Confirm",
                                   f"Are you sure you want to remove {len(post_ids)} posts from this project?"):
            return

        try:
            cursor = self.connection.cursor()

            # Get project ID
            project_id = self.get_project_id(project)

            if not project_id:
                messagebox.showerror("Error", "Project not found")
                return

            # Get the PostAssociation field ID
            cursor.execute("""
                SELECT ID FROM ProjectFields 
                WHERE Project_ID = %s AND Field_Name = 'PostAssociation'
            """, (project_id,))

            field_result = cursor.fetchone()
            if not field_result:
                messagebox.showerror("Error", "Association field not found")
                return

            field_id = field_result[0]

            # Create a placeholder for the query
            placeholders = ', '.join(['%s'] * len(post_ids))

            # Delete the associations
            query = f"""
                DELETE FROM AnalysisResults
                WHERE Project_ID = %s AND Field_ID = %s AND Post_ID IN ({placeholders})
            """

            # Parameters for the query - project_id and field_id, followed by all post_ids
            params = [project_id, field_id] + post_ids

            cursor.execute(query, params)
            rows_affected = cursor.rowcount

            self.connection.commit()

            messagebox.showinfo("Success", f"Removed {rows_affected} posts from the project")

            # Refresh both trees
            self.load_associated_posts()
            self.filter_posts_for_association()

        except mysql.connector.Error as err:
            self.connection.rollback()
            messagebox.showerror("Database Error", f"Error removing posts: {err}")
    def save_post_only(self):
        """Save a post without associating it with any project"""
        sm = self.post_social_media.get()
        user = self.post_username.get()
        text = self.post_post_text.get("1.0", tk.END).strip()
        p_time = self.post_post_time.get()

        if not all([sm, user, text, p_time]):
            messagebox.showerror("Error", "Social Media, Username, Text, and Time are required")
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

            # Get user details from form
            first_name = self.post_user_fname.get() or None
            last_name = self.post_user_lname.get() or None
            birth_country = self.post_birth_country.get() or None
            residence_country = self.post_residence_country.get() or None
            age = self.post_age.get() or None
            gender = self.post_gender.get() or None
            is_verified = self.post_verified_var.get()

            # Handle User - Check if user exists with ANY different details
            cursor.execute("SELECT * FROM User WHERE SM_ID = %s AND Username = %s", (sm_id, user))
            user_result = cursor.fetchone()

            if user_result:
                # User exists - verify ALL details match to ensure consistency
                inconsistencies = []

                # Check each field that has been provided (not empty) for consistency
                if first_name and user_result['First_Name'] != first_name:
                    inconsistencies.append(f"First Name: '{user_result['First_Name']}' vs '{first_name}'")

                if last_name and user_result['Last_Name'] != last_name:
                    inconsistencies.append(f"Last Name: '{user_result['Last_Name']}' vs '{last_name}'")

                if birth_country and user_result['Country_of_Birth'] != birth_country:
                    inconsistencies.append(
                        f"Country of Birth: '{user_result['Country_of_Birth']}' vs '{birth_country}'")

                if residence_country and user_result['Country_of_Residence'] != residence_country:
                    inconsistencies.append(
                        f"Country of Residence: '{user_result['Country_of_Residence']}' vs '{residence_country}'")

                if age and str(user_result['Age']) != age:
                    inconsistencies.append(f"Age: '{user_result['Age']}' vs '{age}'")

                if gender and user_result['Gender'] != gender:
                    inconsistencies.append(f"Gender: '{user_result['Gender']}' vs '{gender}'")

                if user_result['Is_Verified'] != is_verified:
                    inconsistencies.append(
                        f"Verified Status: '{'Yes' if user_result['Is_Verified'] else 'No'}' vs '{'Yes' if is_verified else 'No'}'")

                # If any inconsistencies were found, show detailed error
                if inconsistencies:
                    error_message = f"User '{user}' on {sm} already exists with different details:\n\n"
                    error_message += "\n".join(inconsistencies)
                    error_message += "\n\nTo maintain user data consistency, please use the existing user details or create a new username."

                    # Create a dialog to show the detailed error
                    error_dialog = tk.Toplevel(self.root)
                    error_dialog.title("User Data Consistency Error")
                    error_dialog.geometry("500x300")

                    tk.Label(error_dialog, text=error_message, justify="left", wraplength=480).pack(padx=20, pady=20)

                    # Option to pre-fill fields with existing user data
                    fill_button = ttk.Button(error_dialog, text="Use Existing User Data",
                                             command=lambda: self.fill_user_data(error_dialog, user_result))
                    fill_button.pack(pady=10)

                    ttk.Button(error_dialog, text="Close", command=error_dialog.destroy).pack(pady=10)

                    # Keep dialog on top
                    error_dialog.transient(self.root)
                    error_dialog.grab_set()
                    self.root.wait_window(error_dialog)

                    return
            else:
                # Create new user
                cursor.execute("""
                    INSERT INTO User (SM_ID, Username, First_Name, Last_Name, 
                                   Country_of_Birth, Country_of_Residence, Age, Gender, Is_Verified)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    sm_id, user, first_name, last_name, birth_country,
                    residence_country, age, gender, is_verified
                ))
                self.connection.commit()

            # Check for duplicate posts (same user, same time, same platform)
            cursor.execute("""
                SELECT ID FROM Post 
                WHERE SM_ID = %s AND Username = %s AND Time_Posted = %s
            """, (sm_id, user, p_time))

            post_result = cursor.fetchone()

            if post_result:
                messagebox.showerror(
                    "Duplicate Post",
                    "This user already has a post at this exact time on this platform."
                )
                return
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
                    self.post_city.get() or None,
                    self.post_state.get() or None,
                    self.post_country.get() or None,
                    self.post_likes.get() or 0,
                    self.post_dislikes.get() or 0,
                    self.post_multimedia_var.get()
                ))

                self.connection.commit()

                # Get the ID of the newly created post
                cursor.execute("SELECT LAST_INSERT_ID()")
                post_id = cursor.fetchone()[0]

                messagebox.showinfo("Success", f"Post saved with ID {post_id}")

                # Clear form fields
                self.clear_post_form()

                # Refresh posts list
                self.load_posts()

        except mysql.connector.Error as err:
            self.connection.rollback()
            messagebox.showerror("Database Error", f"Error: {err}")
    def fill_user_data(self, dialog, user_data):
        """Fill the form with existing user data"""
        # Set the form fields to match the existing user data
        self.post_user_fname.delete(0, tk.END)
        self.post_user_fname.insert(0, user_data['First_Name'] or "")

        self.post_user_lname.delete(0, tk.END)
        self.post_user_lname.insert(0, user_data['Last_Name'] or "")

        self.post_birth_country.delete(0, tk.END)
        self.post_birth_country.insert(0, user_data['Country_of_Birth'] or "")

        self.post_residence_country.delete(0, tk.END)
        self.post_residence_country.insert(0, user_data['Country_of_Residence'] or "")

        self.post_age.delete(0, tk.END)
        self.post_age.insert(0, str(user_data['Age']) if user_data['Age'] else "")

        self.post_gender.delete(0, tk.END)
        self.post_gender.insert(0, user_data['Gender'] or "")

        self.post_verified_var.set(user_data['Is_Verified'])

        # Close the dialog
        dialog.destroy()
    def clear_post_form(self):
        """Clear all fields in the post creation form"""
        self.post_username.delete(0, tk.END)
        self.post_user_fname.delete(0, tk.END)
        self.post_user_lname.delete(0, tk.END)
        self.post_birth_country.delete(0, tk.END)
        self.post_residence_country.delete(0, tk.END)
        self.post_age.delete(0, tk.END)
        self.post_gender.delete(0, tk.END)
        self.post_verified_var.set(False)

        self.post_post_time.delete(0, tk.END)
        self.post_city.delete(0, tk.END)
        self.post_state.delete(0, tk.END)
        self.post_country.delete(0, tk.END)
        self.post_likes.delete(0, tk.END)
        self.post_dislikes.delete(0, tk.END)
        self.post_multimedia_var.set(False)

        self.post_post_text.delete("1.0", tk.END)
    def load_posts(self):
        """Load all posts into the posts tree view"""
        try:
            cursor = self.connection.cursor()

            query = """
                SELECT 
                    p.ID as Post_ID,
                    p.Text_Post,
                    sm.Name as Social_Media,
                    p.Username,
                    p.Time_Posted
                FROM Post p
                JOIN SocialMedia sm ON p.SM_ID = sm.ID
                ORDER BY p.Time_Posted DESC
            """

            cursor.execute(query)
            results = cursor.fetchall()

            # Clear existing items
            for item in self.posts_tree.get_children():
                self.posts_tree.delete(item)

            # Add all posts
            for row in results:
                post_id = row[0]
                text = row[1]
                # Truncate text if too long for display
                if len(text) > 50:
                    text = text[:47] + "..."

                self.posts_tree.insert("", "end", values=(
                    post_id,
                    text,
                    row[2],  # Social_Media
                    row[3],  # Username
                    row[4]  # Time_Posted
                ))

            cursor.close()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error loading posts: {err}")
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
                messagebox.showerror("ERROR", f"The reason it failed is because of: {err}")
    def save_project(self):
        proj_name = self.project_name.get()
        manager_first = self.manager_fname.get()
        manager_last = self.manager_lname.get()
        inst_name = self.institution.get()
        start = self.start_date.get()
        end = self.end_date.get()

        if not all([proj_name, manager_first, manager_last, inst_name, start, end]):
            messagebox.showerror("ERROR", "The reason it failed is because not all required fields were filled out")
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
            messagebox.showerror("ERROR","The reason it failed is because either the project or field name was not provided")
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
                SELECT ID, Field_Value FROM AnalysisResults 
                WHERE Project_ID = %s AND Post_ID = %s AND Field_ID = %s
            """, (project_id, post_id_val, field_id))

            result = cursor.fetchone()

            if result:
                # An analysis result already exists for this post/field combination
                existing_value = result[1]
                result_id = result[0]

                if existing_value != value:
                    # If trying to set a different value, show error
                    messagebox.showerror(
                        "Duplicate Analysis",
                        f"This post already has a value '{existing_value}' for field '{field}'. A post cannot have multiple values for the same field in a project."
                    )
                    return
                else:
                    # Same value - inform user
                    messagebox.showinfo("Info", "This analysis value already exists.")
                    return
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
# QUERY FUNCTIONS
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
    def get_posts_by_criteria(self, include_unassociated=False, project_name=None):
        """Get posts based on criteria - can include unassociated posts"""
        # If project name not provided, try to get it from the combined_project field
        if project_name is None:
            project_name = self.combined_project.get().strip()

        # If still no project name and we need one, show error
        if not project_name and not include_unassociated:
            messagebox.showinfo("Notice", "Please select a project first.")
            return []

        try:
            cursor = self.connection.cursor()

            # Different query depending on whether we want to include unassociated posts
            if include_unassociated:
                # Query that gets all posts (associated or not)
                sql = """
                    SELECT 
                        p.ID, 
                        p.Text_Post, 
                        sm.Name AS media, 
                        p.Username, 
                        p.Time_Posted
                    FROM Post p
                    JOIN SocialMedia sm ON p.SM_ID = sm.ID
                """
                # Add project filter if provided
                if project_name:
                    sql += """
                        LEFT JOIN AnalysisResults ar ON p.ID = ar.Post_ID
                        LEFT JOIN Project pr ON ar.Project_ID = pr.ID
                        WHERE pr.Name = %s OR pr.Name IS NULL
                    """
                    cursor.execute(sql, (project_name,))
                else:
                    cursor.execute(sql)
            else:
                # Original query that only gets posts associated with a project
                sql = """
                    SELECT DISTINCT 
                        p.ID, 
                        p.Text_Post, 
                        sm.Name AS media, 
                        p.Username, 
                        p.Time_Posted
                    FROM Post p
                    JOIN SocialMedia sm ON p.SM_ID = sm.ID
                    JOIN AnalysisResults ar ON p.ID = ar.Post_ID
                    JOIN Project pr ON ar.Project_ID = pr.ID
                    WHERE pr.Name = %s
                    ORDER BY p.Time_Posted
                """
                cursor.execute(sql, (project_name,))

            posts = cursor.fetchall()

            # For display in the combined results tree (if used)
            if hasattr(self, 'combined_results_tree'):
                # Clear existing items
                for row in self.combined_results_tree.get_children():
                    self.combined_results_tree.delete(row)

                # Add new items
                for pid, text, media, user, t in posts:
                    self.combined_results_tree.insert("", "end",
                                                      values=(pid, text, media, user, t))

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