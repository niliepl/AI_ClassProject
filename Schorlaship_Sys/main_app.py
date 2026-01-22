import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import subprocess
import tempfile
import sys
import re
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ScholarshipApp:
    def __init__(self, master):
        self.master = master
        master.title("UTP Scholarship Management System")
        master.geometry("1200x800")
        
        # Get the directory where the script is located
        if getattr(sys, 'frozen', False):
            # If the application is run as a bundle (pyinstaller)
            self.script_dir = os.path.dirname(sys.executable)
        else:
            # If the application is run as a script
            self.script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Configuration
        self.responses_filepath = tk.StringVar(value=os.path.join(self.script_dir, "student_responses.csv"))
        self.results_filename = os.path.join(self.script_dir, "scholarship_results.csv")
        self.prolog_filename = os.path.join(self.script_dir, "scholarship_rules.pl")
        self.data_processed = False
        
        # Create main notebook for different interfaces
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.welcome_tab = ttk.Frame(self.notebook)
        self.student_tab = ttk.Frame(self.notebook)
        self.officer_tab = ttk.Frame(self.notebook)
        self.visualization_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.welcome_tab, text="Welcome")
        self.notebook.add(self.student_tab, text="Student Portal")
        self.notebook.add(self.officer_tab, text="Officer Portal")
        self.notebook.add(self.visualization_tab, text="Analytics")
        
        self.setup_welcome_tab()
        self.setup_student_tab()
        self.setup_officer_tab()
        self.setup_visualization_tab()

    def setup_welcome_tab(self):
        """Setup the welcome/landing page"""
        welcome_frame = ttk.Frame(self.welcome_tab, padding="20")
        welcome_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(welcome_frame, text="🎓 UTP Scholarship Management System", 
                 font=('Arial', 24, 'bold')).pack(pady=20)
        
        ttk.Label(welcome_frame, text="AI-Powered Scholarship Eligibility System with Prolog Backend",
                 font=('Arial', 14)).pack(pady=10)
        
        # Show current directory info
        info_text = f"Current working directory: {os.getcwd()}\nScript directory: {self.script_dir}"
        info_label = ttk.Label(welcome_frame, text=info_text, font=('Arial', 9), 
                              background='#f0f0f0', padding=5, justify=tk.LEFT)
        info_label.pack(fill=tk.X, pady=10)
        
        # User type selection
        selection_frame = ttk.Frame(welcome_frame)
        selection_frame.pack(pady=50)
        
        ttk.Label(selection_frame, text="Select Your Role:", font=('Arial', 16)).pack(pady=20)
        
        btn_frame = ttk.Frame(selection_frame)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="👨‍🎓 Student Portal", 
                  command=lambda: self.notebook.select(self.student_tab),
                  width=20, style='Accent.TButton').pack(side=tk.LEFT, padx=10)
        
        ttk.Button(btn_frame, text="👨‍💼 Officer Portal", 
                  command=lambda: self.notebook.select(self.officer_tab),
                  width=20, style='Accent.TButton').pack(side=tk.LEFT, padx=10)
        
        ttk.Button(btn_frame, text="📊 Analytics Dashboard", 
                  command=lambda: self.notebook.select(self.visualization_tab),
                  width=20, style='Accent.TButton').pack(side=tk.LEFT, padx=10)
        
        # Features overview
        features_frame = ttk.LabelFrame(welcome_frame, text="System Features", padding="15")
        features_frame.pack(fill=tk.X, pady=20)
        
        features = [
            "✅ Student Email-Based Result Lookup",
            "✅ Prolog AI Backend Processing",
            "✅ Batch Processing of Applications",
            "✅ Comprehensive Analytics & Visualization",
            "✅ Real-time Decision Making",
            "✅ Multi-criteria Evaluation",
            "✅ Confidence-based Scoring"
        ]
        
        for feature in features:
            ttk.Label(features_frame, text=feature, font=('Arial', 11)).pack(anchor='w', pady=2)

    def setup_student_tab(self):
        """Setup student result lookup interface"""
        main_frame = ttk.Frame(self.student_tab, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Student Result Lookup", 
                 font=('Arial', 18, 'bold')).pack(pady=10)
        
        ttk.Label(main_frame, text="Enter your email to check your scholarship eligibility results", 
                 font=('Arial', 12)).pack(pady=5)
        
        # Email input frame
        email_frame = ttk.LabelFrame(main_frame, text="Enter Your Email", padding="15")
        email_frame.pack(fill=tk.X, pady=20)
        
        ttk.Label(email_frame, text="Email Address:", font=('Arial', 11)).pack(anchor='w', pady=5)
        
        self.student_email = ttk.Entry(email_frame, width=50, font=('Arial', 11))
        self.student_email.pack(fill=tk.X, pady=10)
        
        ttk.Button(email_frame, text="Check My Results", 
                  command=self.check_student_results,
                  style='Accent.TButton').pack(pady=10)
        
        # Results area
        results_frame = ttk.LabelFrame(main_frame, text="Eligibility Results", padding="15")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.student_result_text = tk.Text(results_frame, height=15, wrap=tk.WORD, font=('Arial', 11))
        self.student_result_text.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollbar to results
        scrollbar = ttk.Scrollbar(self.student_result_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.student_result_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.student_result_text.yview)
        
        # Instructions
        instructions = """
📋 Instructions:
1. Enter the email address you used in your scholarship application
2. Click "Check My Results" to view your eligibility decision
3. Your results will show the decision, confidence score, and explanation

Note: Results are only available after the scholarship officer has processed all applications.
        """
        
        info_label = ttk.Label(main_frame, text=instructions, font=('Arial', 10), 
                              background='#f0f0f0', padding=10, justify=tk.LEFT)
        info_label.pack(fill=tk.X, pady=10)

    def setup_officer_tab(self):
        """Setup officer management interface"""
        main_frame = ttk.Frame(self.officer_tab, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Officer Management Portal", 
                 font=('Arial', 18, 'bold')).pack(pady=10)
        
        # File selection
        file_frame = ttk.LabelFrame(main_frame, text="Data Management", padding="10")
        file_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(file_frame, text="Student Responses CSV:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.file_entry = ttk.Entry(file_frame, textvariable=self.responses_filepath, width=60)
        self.file_entry.grid(row=0, column=1, sticky='ew', padx=5, pady=5)
        
        ttk.Button(file_frame, text="Browse", command=self.browse_file).grid(row=0, column=2, padx=5, pady=5)
        
        # Processing buttons
        process_frame = ttk.Frame(file_frame)
        process_frame.grid(row=1, column=0, columnspan=3, sticky='ew', pady=10)
        
        ttk.Button(process_frame, text="🚀 PROCESS WITH PROLOG AI", 
                  command=self.run_prolog_processing,
                  style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(process_frame, text="View Summary", 
                  command=self.display_summary).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(process_frame, text="View Enhanced Results", 
                  command=self.display_detailed_enhanced).pack(side=tk.LEFT, padx=5)
        
        file_frame.columnconfigure(1, weight=1)
        
        # Output area
        self.officer_output_text = tk.Text(main_frame, height=20, wrap=tk.WORD, font=('Courier', 9))
        self.officer_output_text.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.officer_output_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.officer_output_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.officer_output_text.yview)

    def setup_visualization_tab(self):
        """Setup analytics and visualization dashboard"""
        main_frame = ttk.Frame(self.visualization_tab, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Analytics Dashboard", 
                 font=('Arial', 18, 'bold')).pack(pady=10)
        
        # Control frame
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(control_frame, text="Generate All Visualizations", 
                  command=self.generate_all_visualizations,
                  style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(control_frame, text="Refresh Data", 
                  command=self.refresh_visualizations).pack(side=tk.LEFT, padx=5)
        
        # Canvas for plots
        self.viz_frame = ttk.Frame(main_frame)
        self.viz_frame.pack(fill=tk.BOTH, expand=True)
        
        # Initialize with message
        self.viz_label = ttk.Label(self.viz_frame, text="Click 'Generate All Visualizations' to display analytics charts", 
                                  font=('Arial', 12))
        self.viz_label.pack(expand=True)

    def check_student_results(self):
        """Check student results by email using Prolog backend"""
        email = self.student_email.get().strip()
        
        if not email:
            messagebox.showerror("Error", "Please enter your email address.")
            return
        
        if not os.path.exists(self.results_filename):
            messagebox.showwarning("Not Available", 
                                "No results found yet. Please ask the scholarship officer to process the applications first.")
            return
        
        try:
            # Load results and find student by email - FIXED ENCODING
            try:
                results_df = pd.read_csv(self.results_filename, encoding='utf-8')
            except UnicodeDecodeError:
                # Fallback to Windows-1252 if UTF-8 fails
                results_df = pd.read_csv(self.results_filename, encoding='windows-1252')
            
            if 'Email' not in results_df.columns:
                messagebox.showerror("Error", "Results file doesn't contain email information.")
                return
            
            student_result = results_df[results_df['Email'].str.lower() == email.lower()]
            
            if student_result.empty:
                self.student_result_text.delete(1.0, tk.END)
                self.student_result_text.insert(tk.END, f"❌ No results found for email: {email}\n\n")
                self.student_result_text.insert(tk.END, "Please check your email address or contact the scholarship office.")
                return
            
            # Display the result
            result = student_result.iloc[0]
            self.display_student_result_enhanced(result, email)
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not load results: {str(e)}")

    def display_student_result_enhanced(self, result, email):
        """Display individual student result with enhanced user-friendly messages"""
        self.student_result_text.delete(1.0, tk.END)
        
        # Header
        self.student_result_text.insert(tk.END, "🎓 SCHOLARSHIP ELIGIBILITY RESULTS\n", 'header')
        self.student_result_text.insert(tk.END, "=" * 50 + "\n\n")
        self.student_result_text.insert(tk.END, f"📧 Email: {email}\n")
        self.student_result_text.insert(tk.END, f"🆔 Student ID: {result['StudentID']}\n\n")
        
        # Decision with emoji
        decision = result['Decision']
        confidence = result['Confidence']
        explanation = result['Explanation']
        
        self.student_result_text.insert(tk.END, "DECISION: ", 'label')
        if 'Full Scholarship' in decision:
            self.student_result_text.insert(tk.END, f"🟢 {decision}\n", 'success')
        elif 'Partial Scholarship' in decision:
            self.student_result_text.insert(tk.END, f"🟡 {decision}\n", 'partial')
        elif 'Priority Candidate' in decision:
            self.student_result_text.insert(tk.END, f"🟠 {decision}\n", 'priority')
        elif 'Not Eligible' in decision:
            self.student_result_text.insert(tk.END, f"🔴 {decision}\n", 'reject')
        else:
            self.student_result_text.insert(tk.END, f"{decision}\n")
        
        self.student_result_text.insert(tk.END, f"\n📊 CONFIDENCE SCORE: {confidence:.2f}/1.00\n\n", 'label')
        
        # Enhanced Evaluation Details
        self.student_result_text.insert(tk.END, "📋 EVALUATION BREAKDOWN:\n", 'label')
        self.student_result_text.insert(tk.END, "────────────────────────\n")
        
        # Parse and display evaluation details in user-friendly format
        eval_details = self.parse_evaluation_for_student(explanation)
        for detail in eval_details:
            self.student_result_text.insert(tk.END, f"• {detail}\n")
        
        self.student_result_text.insert(tk.END, "\n")
        
        # Enhanced messages based on decision
        self.display_decision_guidance(decision, explanation, confidence)
        
        # Configure text tags for styling
        self.configure_text_tags()

    def parse_evaluation_for_student(self, explanation):
        """Parse explanation into student-friendly bullet points"""
        details = []
        
        try:
            # Academic evaluation
            if 'Academic:' in explanation:
                acad_part = explanation.split('Academic: ')[1].split(' | ')[0]
                tier_match = re.search(r'(\w+) \(([^)]+)\)', acad_part)
                if tier_match:
                    tier = self.get_friendly_tier(tier_match.group(1))
                    details.append(f"📚 Academic Performance: {tier}")
            
            # Financial evaluation
            if 'Financial:' in explanation:
                fin_part = explanation.split('Financial: ')[1].split(' | ')[0]
                level_match = re.search(r'(\w+) \(([^)]+)\)', fin_part)
                if level_match:
                    level = self.get_friendly_financial(level_match.group(1))
                    details.append(f"💰 Financial Need: {level}")
            
            # Activities evaluation
            if 'Activities:' in explanation:
                act_part = explanation.split('Activities: ')[1].split(' | ')[0]
                act_match = re.search(r'(\w+) \(([^)]+)\)', act_part)
                if act_match:
                    level = self.get_friendly_activities(act_match.group(1))
                    details.append(f"🏆 Co-curricular Activities: {level}")
            
            # Special considerations
            if 'Special Factors:' in explanation:
                spec_part = explanation.split('Special Factors: ')[1]
                if spec_part and spec_part != '[]':
                    details.append(f"🎯 Special Circumstances: Considered in evaluation")
                    
        except Exception:
            details = ["Evaluation details available in full report"]
        
        return details

    def display_decision_guidance(self, decision, explanation, confidence):
        """Display appropriate guidance based on decision"""
        if 'Full Scholarship' in decision:
            self.student_result_text.insert(tk.END, 
                "🎉 CONGRATULATIONS!\n\n"
                "You have been awarded a Full Scholarship based on your outstanding application.\n\n"
                "📅 Next Steps:\n"
                "• Official offer letter will be sent to your email within 3 working days\n"
                "• Review and accept the offer through the student portal\n"
                "• Complete any required documentation\n"
                "• Contact scholarship office for any questions\n\n"
                "💡 This scholarship covers tuition fees and provides a living allowance.", 'success_msg')
                
        elif 'Partial Scholarship' in decision:
            self.student_result_text.insert(tk.END,
                "✅ SCHOLARSHIP AWARDED!\n\n"
                "You have been selected for a Partial Scholarship.\n\n"
                "📅 Next Steps:\n"
                "• Scholarship details will be emailed to you\n"
                "• Review the terms and coverage amount\n"
                "• Accept the offer within 14 days\n"
                "• Consider additional financial aid options if needed\n\n"
                "💡 Partial scholarships significantly reduce your educational expenses.", 'partial_msg')
                
        elif 'Priority Candidate' in decision:
            self.student_result_text.insert(tk.END,
                "📋 UNDER SPECIAL CONSIDERATION\n\n"
                "Your application has been marked for priority review.\n\n"
                "📅 What to Expect:\n"
                "• Committee will review your application further\n"
                "• You may be contacted for additional information\n"
                "• Final decision within 7-10 working days\n"
                "• Continue checking your email for updates\n\n"
                "💡 Your unique circumstances are being carefully considered.", 'priority_msg')
                
        elif 'Not Eligible - Basic Requirements' in decision:
            self.student_result_text.insert(tk.END,
                "❌ BASIC ELIGIBILITY NOT MET\n\n"
                "You do not meet the basic eligibility criteria for this scholarship.\n\n", 'reject_msg')
            
            # Show specific basic requirements
            self.student_result_text.insert(tk.END, "Basic Eligibility Requirements:\n", 'label')
            requirements = [
                "• Must be a Malaysian citizen",
                "• Must have no disciplinary record",
                "• Must provide data consent for processing"
            ]
            for req in requirements:
                self.student_result_text.insert(tk.END, f"• {req}\n")
                
            self.student_result_text.insert(tk.END, 
                "\n💡 Unfortunately, you cannot be considered for this scholarship due to the above requirements.\n", 'reject_msg')
                
        elif 'Not Eligible' in decision:
            # Provide specific feedback based on the explanation
            feedback = self.generate_improvement_feedback(explanation)
            self.student_result_text.insert(tk.END,
                "💡 APPLICATION REVIEW COMPLETE\n\n"
                "While you meet basic requirements, your application was not selected this time.\n\n"
                "📊 Areas for Improvement:\n", 'reject_msg')
            
            for item in feedback:
                self.student_result_text.insert(tk.END, f"• {item}\n", 'reject_msg')
                
            self.student_result_text.insert(tk.END,
                "\n🔄 Future Opportunities:\n"
                "• Apply again next semester with improvements\n"
                "• Explore other scholarship programs\n"
                "• Visit Student Affairs for guidance\n"
                "• Consider part-time campus employment\n\n"
                "💡 Many successful students apply multiple times.", 'reject_msg')

    def generate_improvement_feedback(self, explanation):
        """Generate specific improvement suggestions based on evaluation"""
        feedback = []
        
        if 'tier3' in explanation or 'tier4' in explanation:
            feedback.append("Focus on improving your academic performance (aim for CGPA 3.5+)")
        
        if 'minimal' in explanation or 'low' in explanation:
            feedback.append("Limited financial need was a factor in this evaluation")
        
        if 'poor' in explanation or 'basic' in explanation:
            feedback.append("Increase participation in co-curricular activities")
        
        if 'moderate' in explanation:
            feedback.append("Consider taking on leadership roles in student organizations")
        
        if not feedback:
            feedback.append("Competition was high this semester - consider reapplying")
        
        return feedback

    def get_friendly_tier(self, tier):
        """Convert academic tier to friendly name"""
        tier_map = {
            'tier1': 'Excellent', 'tier2': 'Good', 
            'tier3': 'Average', 'tier4': 'Below Average'
        }
        return tier_map.get(tier, tier)

    def get_friendly_financial(self, level):
        """Convert financial level to friendly name"""
        level_map = {
            'urgent': 'Critical Need', 'high': 'High Need',
            'medium': 'Moderate Need', 'low': 'Low Need',
            'minimal': 'Minimal Need'
        }
        return level_map.get(level, level)

    def get_friendly_activities(self, level):
        """Convert activity level to friendly name"""
        level_map = {
            'outstanding': 'Outstanding', 'strong': 'Strong',
            'moderate': 'Moderate', 'basic': 'Basic',
            'poor': 'Limited'
        }
        return level_map.get(level, level)

    def configure_text_tags(self):
        """Configure text styling tags"""
        self.student_result_text.tag_configure('header', font=('Arial', 14, 'bold'), foreground='#2c3e50')
        self.student_result_text.tag_configure('label', font=('Arial', 11, 'bold'), foreground='#34495e')
        self.student_result_text.tag_configure('success', font=('Arial', 12, 'bold'), foreground='#27ae60')
        self.student_result_text.tag_configure('partial', font=('Arial', 12, 'bold'), foreground='#f39c12')
        self.student_result_text.tag_configure('priority', font=('Arial', 12, 'bold'), foreground='#e67e22')
        self.student_result_text.tag_configure('reject', font=('Arial', 12, 'bold'), foreground='#e74c3c')
        self.student_result_text.tag_configure('success_msg', foreground='#27ae60')
        self.student_result_text.tag_configure('partial_msg', foreground='#f39c12')
        self.student_result_text.tag_configure('priority_msg', foreground='#e67e22')
        self.student_result_text.tag_configure('reject_msg', foreground='#e74c3c')

    def browse_file(self):
        """Browse for CSV file"""
        filepath = filedialog.askopenfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filepath:
            self.responses_filepath.set(filepath)
            self.data_processed = False

    def run_prolog_processing(self):
        """Run Prolog backend to process scholarship applications"""
        filepath = self.responses_filepath.get()
        if not filepath or not os.path.exists(filepath):
            messagebox.showerror("Error", "Please select a valid student responses CSV file.")
            return
        
        # Check if Prolog file exists
        if not os.path.exists(self.prolog_filename):
            messagebox.showerror("Error", f"Prolog file not found at:\n{self.prolog_filename}\n\nPlease make sure 'scholarship_rules.pl' is in the same folder as this application.")
            return
        
        try:
            self.officer_output_text.delete(1.0, tk.END)
            self.officer_output_text.insert(tk.END, "🚀 Starting Prolog AI Processing...\n")
            self.officer_output_text.insert(tk.END, f"Script directory: {self.script_dir}\n")
            self.officer_output_text.insert(tk.END, f"Prolog file: {self.prolog_filename}\n")
            self.officer_output_text.insert(tk.END, f"Processing file: {filepath}\n\n")
            self.master.update()
            
            # Convert Windows paths to Prolog compatible paths
            prolog_filepath = filepath.replace('\\', '/')
            prolog_script_path = self.prolog_filename.replace('\\', '/')
            
            # Create a complete Prolog script that includes everything
            complete_script = f"""
% Temporary processing script
:- use_module(library(csv)).
:- use_module(library(lists)).

% Include the actual scholarship rules by reading the file
:- ['{prolog_script_path}'].

% Main execution
main :-
    process_scholarships('{prolog_filepath}'),
    halt.

% Ensure main is called
:- initialization(main).
"""
            
            # Write complete script to temporary file
            temp_script_file = os.path.join(self.script_dir, "temp_complete_script.pl")
            with open(temp_script_file, 'w', encoding='utf-8') as f:
                f.write(complete_script)
            
            # Change to script directory for Prolog execution
            original_cwd = os.getcwd()
            os.chdir(self.script_dir)
            
            # Run Prolog with the temporary script
            result = subprocess.run([
                'swipl', '-q', '-f', 'temp_complete_script.pl'
            ], capture_output=True, text=True, timeout=60, cwd=self.script_dir)
            
            # Change back to original directory
            os.chdir(original_cwd)
            
            # Clean up temporary file
            if os.path.exists(temp_script_file):
                os.remove(temp_script_file)
            
            if result.returncode == 0:
                self.data_processed = True
                self.officer_output_text.insert(tk.END, "✅ PROCESSING COMPLETED SUCCESSFULLY!\n\n")
                self.officer_output_text.insert(tk.END, result.stdout)
                
                # Show summary automatically
                self.display_summary()
                
                messagebox.showinfo("Success", "Prolog AI processing completed successfully!")
            else:
                self.officer_output_text.insert(tk.END, "❌ PROCESSING FAILED!\n\n")
                self.officer_output_text.insert(tk.END, f"Prolog Error Output:\n{result.stderr}\n")
                self.officer_output_text.insert(tk.END, f"Return Code: {result.returncode}\n")
                
                # Also show stdout for debugging
                if result.stdout:
                    self.officer_output_text.insert(tk.END, f"Prolog Output:\n{result.stdout}\n")
                
                messagebox.showerror("Error", "Prolog processing failed. Check the console for details.")
                
        except subprocess.TimeoutExpired:
            self.officer_output_text.insert(tk.END, "❌ PROCESSING TIMEOUT!\n")
            messagebox.showerror("Error", "Processing took too long. Please try again.")
        except Exception as e:
            self.officer_output_text.insert(tk.END, f"❌ ERROR: {str(e)}\n")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def display_summary(self):
        """Display summary statistics"""
        if not os.path.exists(self.results_filename):
            messagebox.showwarning("Warning", "Please process data first or ensure results file exists.")
            return
        
        try:
            try:
                results_df = pd.read_csv(self.results_filename, encoding='utf-8')
            except UnicodeDecodeError:
                results_df = pd.read_csv(self.results_filename, encoding='windows-1252')
            
            summary = {
                'total': len(results_df),
                'full_count': sum(1 for d in results_df['Decision'] if 'Full Scholarship' in d),
                'partial_count': sum(1 for d in results_df['Decision'] if 'Partial Scholarship' in d),
                'priority_count': sum(1 for d in results_df['Decision'] if 'Priority Candidate' in d),
                'not_eligible': sum(1 for d in results_df['Decision'] if 'Not Eligible' in d and 'Basic' not in d),
                'basic_ineligible': sum(1 for d in results_df['Decision'] if 'Basic Requirements' in d),
                'error_count': sum(1 for d in results_df['Decision'] if 'Error' in d),
            }

            output = ["🎓 SCHOLARSHIP EVALUATION SUMMARY", 
                      "=" * 40,
                      f"\nTotal Students Evaluated: {summary['total']}\n",
                      "--- DECISION BREAKDOWN ---"]

            stats = [
                ("🟢 Full Scholarships", summary['full_count']),
                ("🟡 Partial Scholarships", summary['partial_count']),
                ("🟠 Priority Candidates", summary['priority_count']),
                ("🔴 Not Eligible (Criteria)", summary['not_eligible']),
                ("❌ Not Eligible (Basic Requirements)", summary['basic_ineligible']),
                ("⚫ Evaluation Errors", summary['error_count'])
            ]
            
            for label, count in stats:
                output.append(f"{label:<40}: {count}")

            output.append("\n---")
            output.append("💡 Students can now check their results using their email in the Student Portal")
            
            self.officer_output_text.delete(1.0, tk.END)
            self.officer_output_text.insert(tk.END, '\n'.join(output))
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not load results: {str(e)}")

    def display_detailed_enhanced(self):
        """Display detailed results with user-friendly formatting"""
        if not os.path.exists(self.results_filename):
            messagebox.showwarning("Warning", "Please process data first.")
            return

        try:
            try:
                results_df = pd.read_csv(self.results_filename, encoding='utf-8')
            except UnicodeDecodeError:
                results_df = pd.read_csv(self.results_filename, encoding='windows-1252')
            
            output = ["🎓 DETAILED SCHOLARSHIP ANALYSIS (Grouped by Decision)\n"]
            output.append("=" * 80)
            
            # Group by decision in specific order
            decision_order = ['Full Scholarship', 'Partial Scholarship', 'Priority Candidate', 
                            'Not Eligible', 'Not Eligible - Basic Requirements']
            
            for decision in decision_order:
                group = results_df[results_df['Decision'] == decision]
                if len(group) > 0:
                    # Header with count
                    if 'Full Scholarship' in decision:
                        header = f"🌟 {decision.upper()} ({len(group)} Students)"
                    elif 'Partial Scholarship' in decision:
                        header = f"✅ {decision.upper()} ({len(group)} Students)"
                    elif 'Priority Candidate' in decision:
                        header = f"📋 {decision.upper()} ({len(group)} Students)"
                    else:
                        header = f"❌ {decision.upper()} ({len(group)} Students)"
                    
                    output.append(f"\n{header}")
                    output.append("-" * 60)
                    
                    for _, row in group.iterrows():
                        email = row['Email'] if 'Email' in row else 'N/A'
                        conf = f"{row['Confidence']:.2f}"
                        explanation = self.parse_explanation_for_display(row['Explanation'])
                        
                        output.append(f"\n📧 {email}")
                        output.append(f"   Confidence: {conf}")
                        output.append(f"   {explanation}")
                    
                    output.append("")  # Empty line between groups

            self.officer_output_text.delete(1.0, tk.END)
            self.officer_output_text.insert(tk.END, '\n'.join(output))
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not load detailed results: {str(e)}")

    def parse_explanation_for_display(self, explanation):
        """Parse the technical explanation into user-friendly format"""
        try:
            parts = []
            
            # Academic part
            if 'Academic:' in explanation:
                acad_part = explanation.split('Academic: ')[1].split(' | ')[0]
                tier_match = re.search(r'(\w+) \(([^)]+)\)', acad_part)
                if tier_match:
                    tier = tier_match.group(1)
                    details = tier_match.group(2)
                    parts.append(f"📚 Academic: {self.get_friendly_tier(tier)} ({details})")
            
            # Financial part
            if 'Financial:' in explanation:
                fin_part = explanation.split('Financial: ')[1].split(' | ')[0]
                level_match = re.search(r'(\w+) \(([^)]+)\)', fin_part)
                if level_match:
                    level = level_match.group(1)
                    details = level_match.group(2)
                    parts.append(f"💰 Financial: {self.get_friendly_financial(level)} ({details})")
            
            # Activities part
            if 'Activities:' in explanation:
                act_part = explanation.split('Activities: ')[1].split(' | ')[0]
                act_match = re.search(r'(\w+) \(([^)]+)\)', act_part)
                if act_match:
                    level = act_match.group(1)
                    details = act_match.group(2)
                    parts.append(f"🏆 Activities: {self.get_friendly_activities(level)} ({details})")
            
            # Special factors
            if 'Special Factors:' in explanation:
                spec_part = explanation.split('Special Factors: ')[1]
                if spec_part and spec_part != '[]':
                    parts.append(f"🎯 Special Considerations: {spec_part}")
            
            return " | ".join(parts)
            
        except Exception:
            return explanation  # Fallback to original if parsing fails

    def generate_all_visualizations(self):
        """Generate and display all visualizations - IMPROVED LAYOUT"""
        if not os.path.exists(self.results_filename):
            messagebox.showwarning("Warning", "Please process data first to generate visualizations.")
            return

        try:
            # Clear previous visualizations
            for widget in self.viz_frame.winfo_children():
                widget.destroy()

            try:
                df = pd.read_csv(self.results_filename, encoding='utf-8')
            except UnicodeDecodeError:
                df = pd.read_csv(self.results_filename, encoding='windows-1252')
        
            # Create feature engineering for visualizations
            df['Academic_Tier'] = df['Explanation'].str.extract(r'Academic: (\w+)')
            df['Financial_Level'] = df['Explanation'].str.extract(r'Financial: (\w+)')
            df['Activity_Level'] = df['Explanation'].str.extract(r'Activities: (\w+)')
            df_filtered = df[df['Academic_Tier'].notna() & (df['Confidence'] > 0)].copy()

            # Create a scrollable frame for visualizations
            canvas = tk.Canvas(self.viz_frame)
            scrollbar = ttk.Scrollbar(self.viz_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            # Create matplotlib figures - BETTER LAYOUT
            fig1, ax1 = plt.subplots(figsize=(12, 6))
            fig2, ax2 = plt.subplots(figsize=(12, 6))
            fig3, ax3 = plt.subplots(figsize=(12, 6))
            fig4, ax4 = plt.subplots(figsize=(12, 6))
            fig5, ax5 = plt.subplots(figsize=(12, 6))

            # Chart 1: Distribution of Decisions
            decision_counts = df['Decision'].value_counts()
            colors = ['#2ecc71', '#f39c12', '#e67e22', '#e74c3c', '#95a5a6', '#34495e']
            sns.barplot(y=decision_counts.index, x=decision_counts.values, ax=ax1, palette=colors[:len(decision_counts)])
            ax1.set_title('1. Distribution of Scholarship Decisions', fontsize=14, fontweight='bold', pad=20)
            ax1.set_xlabel('Number of Students', fontsize=12)
            ax1.set_ylabel('Decision', fontsize=12)
            ax1.tick_params(axis='y', labelsize=10)
            
            # Add value labels on bars
            for i, v in enumerate(decision_counts.values):
                ax1.text(v + 0.1, i, str(v), color='black', fontweight='bold', va='center')

            # Chart 2: Confidence by Decision
            sns.boxplot(x='Decision', y='Confidence', data=df, ax=ax2, palette='Set2')
            ax2.set_title('2. Confidence Score by Decision', fontsize=14, fontweight='bold', pad=20)
            ax2.set_xlabel('Decision', fontsize=12)
            ax2.set_ylabel('Confidence Score', fontsize=12)
            ax2.tick_params(axis='x', rotation=45, labelsize=10)
            ax2.tick_params(axis='y', labelsize=10)
            
            # Add mean value annotations
            for i, decision in enumerate(df['Decision'].unique()):
                mean_val = df[df['Decision'] == decision]['Confidence'].mean()
                ax2.text(i, mean_val + 0.02, f'μ={mean_val:.2f}', 
                        ha='center', va='bottom', fontweight='bold', fontsize=9)

            # Chart 3: Decisions by Academic Tier
            if not df_filtered.empty:
                decision_by_tier = pd.crosstab(df_filtered['Academic_Tier'], df_filtered['Decision'])
                tier_order = ['tier1', 'tier2', 'tier3']
                existing_tiers = [t for t in tier_order if t in decision_by_tier.index]
                if existing_tiers:
                    decision_by_tier.reindex(existing_tiers, fill_value=0).plot(
                        kind='bar', stacked=True, ax=ax3, colormap='viridis')
                    ax3.set_title('3. Decisions by Academic Tier', fontsize=14, fontweight='bold', pad=20)
                    ax3.set_xlabel('Academic Tier', fontsize=12)
                    ax3.set_ylabel('Number of Students', fontsize=12)
                    ax3.legend(title='Decision', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
                    ax3.tick_params(axis='x', rotation=0, labelsize=10)
                    ax3.tick_params(axis='y', labelsize=10)

            # Chart 4: Decisions by Financial Level
            if not df_filtered.empty:
                decision_by_financial = pd.crosstab(df_filtered['Financial_Level'], df_filtered['Decision'])
                financial_order = ['minimal', 'low', 'medium', 'high', 'urgent']
                existing_financial = [f for f in financial_order if f in decision_by_financial.index]
                if existing_financial:
                    decision_by_financial.reindex(existing_financial, fill_value=0).plot(
                        kind='bar', stacked=True, ax=ax4, colormap='plasma')
                    ax4.set_title('4. Decisions by Financial Level', fontsize=14, fontweight='bold', pad=20)
                    ax4.set_xlabel('Financial Level', fontsize=12)
                    ax4.set_ylabel('Number of Students', fontsize=12)
                    ax4.legend(title='Decision', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
                    ax4.tick_params(axis='x', rotation=0, labelsize=10)
                    ax4.tick_params(axis='y', labelsize=10)

            # Chart 5: Decisions by Activity Level
            if not df_filtered.empty:
                decision_by_activity = pd.crosstab(df_filtered['Activity_Level'], df_filtered['Decision'])
                activity_order = ['poor', 'basic', 'moderate', 'strong', 'outstanding']
                existing_activity = [a for a in activity_order if a in decision_by_activity.index]
                if existing_activity:
                    decision_by_activity.reindex(existing_activity, fill_value=0).plot(
                        kind='bar', stacked=True, ax=ax5, colormap='Set1')
                    ax5.set_title('5. Decisions by Activity Level', fontsize=14, fontweight='bold', pad=20)
                    ax5.set_xlabel('Activity Level', fontsize=12)
                    ax5.set_ylabel('Number of Students', fontsize=12)
                    ax5.legend(title='Decision', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
                    ax5.tick_params(axis='x', rotation=0, labelsize=10)
                    ax5.tick_params(axis='y', labelsize=10)

            # Adjust layout for all figures
            for fig, title in [(fig1, "Decision Distribution"), (fig2, "Confidence Analysis"), 
                            (fig3, "Academic Tier Analysis"), (fig4, "Financial Level Analysis"), 
                            (fig5, "Activity Level Analysis")]:
                fig.tight_layout(pad=3.0)

            # Embed figures in scrollable frame
            figures = [(fig1, "Decision Distribution"), (fig2, "Confidence Analysis"), 
                    (fig3, "Academic Tier Analysis"), (fig4, "Financial Level Analysis"), 
                    (fig5, "Activity Level Analysis")]

            for i, (fig, title) in enumerate(figures):
                # Create a frame for each chart
                chart_frame = ttk.LabelFrame(scrollable_frame, text=title, padding="10")
                chart_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
                
                # Embed the figure
                canvas_fig = FigureCanvasTkAgg(fig, chart_frame)
                canvas_fig.draw()
                canvas_fig.get_tk_widget().pack(fill=tk.BOTH, expand=True)
                
                # Add a separator between charts (except the last one)
                if i < len(figures) - 1:
                    ttk.Separator(scrollable_frame, orient='horizontal').pack(fill=tk.X, padx=10, pady=5)

            # Pack canvas and scrollbar
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            messagebox.showinfo("Success", "All 5 visualizations generated successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Could not generate visualizations: {str(e)}")

    def refresh_visualizations(self):
        """Refresh visualization data"""
        self.generate_all_visualizations()

def main():
    root = tk.Tk()
    app = ScholarshipApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()