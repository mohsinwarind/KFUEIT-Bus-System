# KFUEIT Bus System

## Introduction

For my final capstone project for CS50 Web App Development, I chose to create a dynamic and flexible bus route system tailored to my university's requirements. I often use buses because they are convenient as I can read my books while listening to piano music from a window seat and more importantly they are environmentally friendly. However, the department of transport of my Univrsity was using an outdated system, managing everything with Excel and converting it into PDFs to share among students.So, one day when I was looking onto the timetable , I came up with this idea of making this dynamic , user-friendly , responsive and Administrative independent platform to manage buses route system.

## Distinctiveness and Complexity

Compared to previous projects I've done for this course, this one is unique and complex for several reasons:

1. The old `CS50W Pizza Project` was quite cliché and similar to previous projects, making it less challenging. In contrast, this project involves up to eight models, adding significant complexity.
2. Unlike the project network, which included a profile template only for bus drivers, this project features independent parts that collectively form a comprehensive system. We will explore these parts shortly.
3. This is not an e-commerce store—there's no cart or selling involved. Instead, it’s a timetable system with additional support for reporting missing items so that if someone finds them, they can contact the person directly to return them. There's no element of capitalism here.
4. The three main parts of this app include:
   - The timetable for buses: Students with access can log in and create their own timetable, independent of the university transport office.
   - Missing item complaints: Users can report lost personal belongings, and others who find them can view the complaints and contact the owner.
   - Driver information and reviews: Users can review bus drivers, which helps ensure credibility and accountability. Poor ratings for overspeeding or unmet responsibilities can affect the driver's rating.
   - Live Tracking System :  Students/User can see the live location of buses to see how far they are .
So these things collectively make this project novel with respect to the preceding projects.
## Breakdown of Each File

### 1. `models.py`

- **User**
  - **Description:** Extends Django's default user model without additional fields.
  - **Purpose:** Provides basic user authentication; can be customized later which was not needed here in this project.

- **BusRoute**
  - **Fields:** `name` (unique `CharField`).
  - **Purpose:** Represents a bus route, identified by a unique name.
  - **String Representation:** Returns the route name.

- **StopPoint**
  - **Fields:** `name` (unique `CharField`).
  - **Purpose:** Represents a bus stop, identified by a unique name.
  - **String Representation:** Returns the stop name.

- **PickupPoint**
  - **Fields:** `bus_route` (ForeignKey to `BusRoute`), `stop_point` (ForeignKey to `StopPoint`), `time` (optional `CharField` with 24-hour format).
  - **Purpose:** Represents a bus route’s pickup location and time.
  - **String Representation:** Returns a formatted string with stop point, route name, and pickup time.

- **DropPoint**
  - **Fields:** `bus_route` (ForeignKey to `BusRoute`), `stop_point` (ForeignKey to `StopPoint`), `time` (optional `CharField` with 24-hour format).
  - **Purpose:** Represents a bus route’s drop-off location and time.
  - **String Representation:** Returns a formatted string with stop point, route name, and drop-off time.

- **MissingComplaint**
  - **Fields:** `student` (ForeignKey to `User`), `item_name`, `description`, `location`, `date_lost`, `image` (optional), `status` (choices: pending, found, not found), `date_reported`, `contact_email` (optional), `contact_phone` (optional).
  - **Purpose:** Tracks missing items reported by users.
  - **String Representation:** Returns a string with item name and status.

- **BusDriver**
  - **Fields:** `name`, `years_of_service`, `cnic_number` (unique), `contact_number`, `blood_group`, `rating` (DecimalField), `image` (optional).
  - **Purpose:** Represents a bus driver with personal and service details.
  - **String Representation:** Returns the driver’s name.

- **DriverReview**
  - **Fields:** `driver` (ForeignKey to `BusDriver`), `student` (ForeignKey to `User`), `rating`, `review_text`, `created_at`.
  - **Purpose:** Allows users to rate and review bus drivers.
  - **String Representation:** Returns a string with the student's username and driver’s name.

### 2. `forms.py`

This file serves an integral role in creating forms and helping store the raw data in the database using the graphical user interface.

- **BusRouteForm**
  - **Description:** A form for creating and updating `BusRoute` instances, with a single field for the route name.

- **MissingComplaintForm**
  - **Description:** A form for reporting missing items, including fields for item details, location, date lost, an optional image, and contact information.

- **DriverReviewForm**
  - **Description:** A form for submitting reviews and ratings for bus drivers, with a text area for review comments.

### 3. `views.py`

Here’s a breakdown of the view methods used in this app:

- **index:** Displays the first three bus routes and drivers on the homepage.
- **login_view:** Handles user login; redirects on success or shows an error on failure.
- **register:** Registers a new user and logs them in if successful; shows an error if usernames are taken or passwords don’t match.
- **logout_view:** Logs out the current user and redirects to the homepage.
- **bus_route_form_view:** Handles creating and updating bus routes with pickup and drop-off points; displays form and processes submissions.
- **bus_route_detail_view:** Shows details of a specific bus route, including pickup and drop-off points.
- **update_route:** Updates an existing bus route with new pickup and drop-off data via JSON; responds with success or error.
- **delete_bus_route:** Deletes a bus route and redirects to the homepage; shows a success message.
- **report_and_view_missing_items:** Allows users to report and view their missing items; handles form submissions and displays complaints.
- **edit_missing_item:** Allows users to edit their missing item complaints; processes form submissions.
- **delete_missing_item:** Deletes a missing item complaint and returns a JSON response.
- **update_missing_item_status:** Updates the status of a missing item complaint via POST request and returns a JSON response.
- **driver_profile:** Displays a bus driver’s profile with reviews; allows users to submit a review and updates driver rating.
- **all_routes:** Lists all bus routes.
- **all_missing_complaints:** Lists all missing item complaints.
- **all_drivers:** Lists all bus drivers.

### 4. `validator.py`

This file contains a function named `validate_24_hour_format`, which validates that a given string represents a valid time in 24-hour HHMM format (e.g., "1345" for 1:45 PM). It uses a regular expression to check if the time string matches the format and raises a `ValidationError` with a message if it does not.

### 5. Templates and Static Files

Each template has its respective CSS file, and JavaScript is also separated where needed in the static folder. Images for media, such as profile pictures of drivers and images of missing items, are stored separately in a two folder located in the main directory.

### Additional Information
Let me share you the key features of this app
1. **Bus Timetable Flexibility:** You can add as many rows and columns as needed, allowing for dynamic management of the timetable.
2. **Editing Details:** You can edit the details of the timetable via the view table page, but you must be logged in to make changes.
3. **Modifying Tables:** To add columns or rows to an existing table, you must select the preexisting route. New entries will append to the end. To add something in between, you need to delete the existing route and create it from scratch with the desired number of columns.
4. **Driver Ratings:** Drivers can be rated out of five stars, but you need to be logged in to submit a rating.
5. **Responsive Design:** All pages are made responsive using Bootstrap 5 and CSS.
6. **Photo Upload:** Users can upload photos from their devices, a feature not covered in previous courses.
7. **Complaint Option:** If a student lost his personal belongings while using bus , they can add up a post with a photo (optinal) which can help to create a community that can help each other finding the lost thing. And if someone find that , it can easily contact the owner and return them.
## Steps to Run the Application

1. **Download or Clone:**
   - Download the zip file or clone it via GitHub.

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt

3. **Navigate to Directory:**
   ```bash
   cd KFUEITBUSSYSTEM

4. **Apply Migrations:**
   ```bash
   python manage.py makemigrations BusRoute
   python manage.py migrate

5. **Run the Development Server:**
   ```bash
   python manage.py runserver
6. **Access the Application::**
    - Open a web browser and navigate to `http://127.0.0.1:8000/` (or the port you specified) to see your Django application in action.
  
---
<br>

```
That's all from my side
Happy Coding :)
```
