import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import sqlite3
from tkinter import scrolledtext

class HospitalManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management System")

        # Create database connection
        self.conn = sqlite3.connect('hospital.db')
        self.cur = self.conn.cursor()

        # Create doctor table
        self.cur.execute('''CREATE TABLE IF NOT EXISTS doctors (
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            specialization TEXT,
                            phone_number TEXT
                            )''')

        # Create patient table
        self.cur.execute('''CREATE TABLE IF NOT EXISTS patients (
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            gender TEXT,
                            age INTEGER,
                            email TEXT,
                            phone_number TEXT
                            )''')


        # Create appointment table
        self.cur.execute('''CREATE TABLE IF NOT EXISTS appointments (
                            id INTEGER PRIMARY KEY,
                            doctor_id INTEGER,
                            patient_id INTEGER,
                            date TEXT,
                            time TEXT,
                            FOREIGN KEY(doctor_id) REFERENCES doctors(id),
                            FOREIGN KEY(patient_id) REFERENCES patients(id)
                            )''')

        # Create tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        # Add tabs
        self.add_doctor_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.add_doctor_tab, text='Add Doctor')
        self.add_patient_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.add_patient_tab, text='Add Patient')
        self.add_appointment_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.add_appointment_tab, text='Add Appointment')
        self.list_doctors_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.list_doctors_tab, text='List Doctors')
        self.list_patients_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.list_patients_tab, text='List Patients')
        self.list_appointments_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.list_appointments_tab, text='List Appointments')

        # Add Doctor Tab
        self.add_doctor_label = ttk.Label(self.add_doctor_tab, text="Enter Doctor's Name:")
        self.add_doctor_label.pack()
        self.add_doctor_entry = ttk.Entry(self.add_doctor_tab)
        self.add_doctor_entry.pack()
        self.add_specialization_label = ttk.Label(self.add_doctor_tab, text="Enter Doctor's Specialization:")
        self.add_specialization_label.pack()
        self.add_specialization_entry = ttk.Entry(self.add_doctor_tab)
        self.add_specialization_entry.pack()
        self.add_phone_number_label = ttk.Label(self.add_doctor_tab, text="Enter Doctor's Phone Number:")
        self.add_phone_number_label.pack()
        self.add_phone_number_entry = ttk.Entry(self.add_doctor_tab)
        self.add_phone_number_entry.pack()
        self.add_doctor_button = ttk.Button(self.add_doctor_tab, text="Add Doctor", command=self.add_doctor)
        self.add_doctor_button.pack()

        # Add Patient Tab
        self.add_patient_label = ttk.Label(self.add_patient_tab, text="Enter Patient's Name:")
        self.add_patient_label.pack()
        self.add_patient_entry = ttk.Entry(self.add_patient_tab)
        self.add_patient_entry.pack()

        self.age_label = ttk.Label(self.add_patient_tab, text="Enter Patient's Age:")
        self.age_label.pack()
        self.age_entry = ttk.Entry(self.add_patient_tab)
        self.age_entry.pack()

        self.gender_frame = ttk.LabelFrame(self.add_patient_tab, text="Select Patient's Gender")
        self.gender_frame.pack()

        self.gender_var = tk.StringVar()
        self.gender_var.set("Male")
        self.male_radio = ttk.Radiobutton(self.gender_frame, text="Male", variable=self.gender_var, value="Male")
        self.male_radio.grid(row=0, column=0, padx=5, pady=5)
        self.female_radio = ttk.Radiobutton(self.gender_frame, text="Female", variable=self.gender_var, value="Female")
        self.female_radio.grid(row=0, column=1, padx=5, pady=5)
        self.other_radio = ttk.Radiobutton(self.gender_frame, text="Other", variable=self.gender_var, value="Other")
        self.other_radio.grid(row=0, column=2, padx=5, pady=5)

        self.email_label = ttk.Label(self.add_patient_tab, text="Enter Patient's Email:")
        self.email_label.pack()
        self.email_entry = ttk.Entry(self.add_patient_tab)
        self.email_entry.pack()

        self.phone_number_patient_label = ttk.Label(self.add_patient_tab, text="Enter Patient's Phone Number:")
        self.phone_number_patient_label.pack()
        self.phone_number_patient_entry = ttk.Entry(self.add_patient_tab)
        self.phone_number_patient_entry.pack()

        self.add_patient_button = ttk.Button(self.add_patient_tab, text="Add Patient", command=self.add_patient)
        self.add_patient_button.pack()

        # Add Appointment Tab
        self.doctor_label = ttk.Label(self.add_appointment_tab, text="Select Doctor:")
        self.doctor_label.pack()
        self.doctor_var = tk.StringVar()
        self.doctor_dropdown = ttk.Combobox(self.add_appointment_tab, textvariable=self.doctor_var)
        self.doctor_dropdown.pack()
        self.patient_label = ttk.Label(self.add_appointment_tab, text="Select Patient:")
        self.patient_label.pack()
        self.patient_var = tk.StringVar()
        self.patient_dropdown = ttk.Combobox(self.add_appointment_tab, textvariable=self.patient_var)
        self.patient_dropdown.pack()
        self.date_label = ttk.Label(self.add_appointment_tab, text="Select Date:")
        self.date_label.pack()
        self.cal = DateEntry(self.add_appointment_tab, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.cal.pack(padx=10, pady=10)
        self.time_label = ttk.Label(self.add_appointment_tab, text="Select Time:")
        self.time_label.pack()
        self.time_frame = ttk.Frame(self.add_appointment_tab)
        self.time_frame.pack()
        self.hours = [str(i).zfill(2) for i in range(24)]
        self.minutes = [str(i).zfill(2) for i in range(0, 60, 15)]
        self.hour_var = tk.StringVar()
        self.minute_var = tk.StringVar()
        self.hour_dropdown = ttk.Combobox(self.time_frame, textvariable=self.hour_var, values=self.hours)
        self.hour_dropdown.grid(row=0, column=0)
        self.hour_dropdown.set('12')
        self.minute_dropdown = ttk.Combobox(self.time_frame, textvariable=self.minute_var, values=self.minutes)
        self.minute_dropdown.grid(row=0, column=1)
        self.minute_dropdown.set('00')
        self.add_appointment_button = ttk.Button(self.add_appointment_tab, text="Add Appointment", command=self.add_appointment)
        self.add_appointment_button.pack()

        # List Doctors Tab
        self.list_doctors_tree = ttk.Treeview(self.list_doctors_tab, columns=('Name', 'Specialization', 'Phone Number'))
        self.list_doctors_tree.heading('#0', text='ID')
        self.list_doctors_tree.column('#0', width=50, anchor='center')
        self.list_doctors_tree.heading('Name', text='Name')
        self.list_doctors_tree.column('Name', width=150)
        self.list_doctors_tree.heading('Specialization', text='Specialization')
        self.list_doctors_tree.column('Specialization', width=150)
        self.list_doctors_tree.heading('Phone Number', text='Phone Number')
        self.list_doctors_tree.column('Phone Number', width=150)
        self.list_doctors_tree.pack(fill='both', expand=True)

        # List Patients Tab
        self.list_patients_tree = ttk.Treeview(self.list_patients_tab, columns=('Name', 'Gender', 'Age', 'Phone Number', 'Address'))
        self.list_patients_tree.heading('#0', text='ID')
        self.list_patients_tree.column('#0', width=50, anchor='center')
        self.list_patients_tree.heading('Name', text='Name')
        self.list_patients_tree.column('Name', width=150)
        self.list_patients_tree.heading('Gender', text='Gender')
        self.list_patients_tree.column('Gender', width=100)
        self.list_patients_tree.heading('Age', text='Age')
        self.list_patients_tree.column('Age', width=100)
        self.list_patients_tree.heading('Phone Number', text='Phone Number')
        self.list_patients_tree.column('Phone Number', width=150)
        self.list_patients_tree.heading('Address', text='Address')
        self.list_patients_tree.column('Address', width=200)
        self.list_patients_tree.pack(fill='both', expand=True)

        # List Appointments Tab
        self.list_appointments_tree = ttk.Treeview(self.list_appointments_tab, columns=('Doctor', 'Patient', 'Date', 'Time'))
        self.list_appointments_tree.heading('#0', text='ID')
        self.list_appointments_tree.column('#0', width=50, anchor='center')
        self.list_appointments_tree.heading('Doctor', text='Doctor')
        self.list_appointments_tree.column('Doctor', width=150)
        self.list_appointments_tree.heading('Patient', text='Patient')
        self.list_appointments_tree.column('Patient', width=150)
        self.list_appointments_tree.heading('Date', text='Date')
        self.list_appointments_tree.column('Date', width=100, anchor='center')
        self.list_appointments_tree.heading('Time', text='Time')
        self.list_appointments_tree.column('Time', width=100, anchor='center')
        self.list_appointments_tree.pack(fill='both', expand=True)

        self.update_doctor_list()
        self.doctor_dropdown['values'] = self.doctor_names

        self.update_patient_list()
        self.patient_dropdown['values'] = self.patient_names

        self.list_doctors()
        self.list_patients()
        self.list_appointments()

    def update_doctor_list(self):
        self.cur.execute("SELECT * FROM doctors")
        self.doctors = self.cur.fetchall()
        self.doctor_names = [doctor[1] for doctor in self.doctors]

    def update_patient_list(self):
        self.cur.execute("SELECT * FROM patients")
        self.patients = self.cur.fetchall()
        self.patient_names = [patient[1] for patient in self.patients]

    def add_doctor(self):
        doctor_name = self.add_doctor_entry.get()
        specialization = self.add_specialization_entry.get()
        phone_number = self.add_phone_number_entry.get()
        if doctor_name:
            self.cur.execute("INSERT INTO doctors (name, specialization, phone_number) VALUES (?, ?, ?)", (doctor_name, specialization, phone_number))
            self.conn.commit()
            self.update_doctor_list()
            self.doctor_dropdown['values'] = self.doctor_names
            self.list_doctors()
            messagebox.showinfo("Success", "Doctor information added successfully!")
            
            self.add_doctor_entry.delete(0, tk.END)
            self.add_specialization_entry.delete(0, tk.END)
            self.add_phone_number_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Incomplete Information", "Please fill in all fields.")


    def add_patient(self):
        patient_name = self.add_patient_entry.get()
        age = self.age_entry.get()
        gender = self.gender_var.get()
        email = self.email_entry.get()
        phone_number = self.phone_number_patient_entry.get()
        if patient_name and age and gender and email and phone_number:
            self.cur.execute("INSERT INTO patients (name, age, gender, email, phone_number) VALUES (?, ?, ?, ?, ?)", (patient_name, age, gender, email, phone_number))
            self.conn.commit()
            self.update_patient_list()
            self.patient_dropdown['values'] = self.patient_names
            self.list_patients()
            messagebox.showinfo("Success", "Patient information added successfully!")
            self.add_patient_entry.delete(0, tk.END)
            self.age_entry.delete(0, tk.END)
            self.gender_var.set("Male")
            self.email_entry.delete(0, tk.END)
            self.phone_number_patient_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Incomplete Information", "Please fill in all fields.")

    def add_appointment(self):
        doctor_name = self.doctor_var.get()
        patient_name = self.patient_var.get()
        appointment_date = self.cal.get()
        appointment_time = f"{self.hour_var.get()}:{self.minute_var.get()}"

        if doctor_name and patient_name and appointment_date:
            doctor_id = [doctor[0] for doctor in self.doctors if doctor[1] == doctor_name][0]
            patient_id = [patient[0] for patient in self.patients if patient[1] == patient_name][0]

            self.cur.execute("INSERT INTO appointments (doctor_id, patient_id, date, time) VALUES (?, ?, ?, ?)", (doctor_id, patient_id, appointment_date, appointment_time))
            self.conn.commit()
            messagebox.showinfo("Appointment Added", f"Appointment for {patient_name} with {doctor_name} on {appointment_date} at {appointment_time} added.")
            self.list_appointments()

    def list_doctors(self, event=None):
        self.list_doctors_tree.delete(*self.list_doctors_tree.get_children())
        for doctor in self.doctors:
            self.list_doctors_tree.insert('', 'end', text=doctor[0], values=(doctor[1], doctor[2], doctor[3]))

    def list_patients(self, event=None):
        self.list_patients_tree.delete(*self.list_patients_tree.get_children())
        for patient in self.patients:
            self.list_patients_tree.insert('', 'end', text=patient[0], values=(patient[1], patient[2], patient[3], patient[4], patient[5]))

    def list_appointments(self, event=None):
        self.list_appointments_tree.delete(*self.list_appointments_tree.get_children())
        self.cur.execute('''SELECT appointments.id, doctors.name AS doctor, patients.name AS patient, appointments.date, appointments.time
                            FROM appointments
                            JOIN doctors ON appointments.doctor_id = doctors.id
                            JOIN patients ON appointments.patient_id = patients.id''')
        appointments = self.cur.fetchall()
        for appointment in appointments:
            self.list_appointments_tree.insert('', 'end', text=appointment[0], values=(appointment[1], appointment[2], appointment[3], appointment[4]))

    def __del__(self):
        self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = HospitalManagementApp(root)
    root.mainloop()

