from flask import Flask, render_template, request, redirect, url_for, flash, Response
import io
import csv
from datetime import datetime

app = Flask(__name__)
# A secret key is needed for flashing messages
app.secret_key = 'supersecretkey'

# SDG Titles for tooltips
SDG_TITLES = {
    1: 'No Poverty',
    2: 'Zero Hunger',
    3: 'Good Health and Well-being',
    4: 'Quality Education',
    5: 'Gender Equality',
    6: 'Clean Water and Sanitation',
    7: 'Affordable and Clean Energy',
    8: 'Decent Work and Economic Growth',
    9: 'Industry, Innovation and Infrastructure',
    10: 'Reduced Inequality',
    11: 'Sustainable Cities and Communities',
    12: 'Responsible Consumption and Production',
    13: 'Climate Action',
    14: 'Life Below Water',
    15: 'Life on Land',
    16: 'Peace and Justice Strong Institutions',
    17: 'Partnerships to achieve the Goal'
}

# Official SDG colors (without '#') for shields.io badges
SDG_COLORS = {
    1: 'E5243B',
    2: 'DDA63A',
    3: '4C9F38',
    4: 'C5192D',
    5: 'FF3A21',
    6: '26BDE2',
    7: 'FCC30B',
    8: 'A21942',
    9: 'FD6925',
    10: 'DD1367',
    11: 'FD9D24',
    12: 'BF8B2E',
    13: '3F7E44',
    14: '0A97D9',
    15: '56C02B',
    16: '00689D',
    17: '19486A'
}

@app.context_processor
def inject_sdg_data():
    """Injects SDG data into all templates."""
    return dict(sdg_titles=SDG_TITLES, sdg_colors=SDG_COLORS)


# Expanded mock data
ngo_impact_data = [
    {
        'id': 1,
        'slug': 'green-future-foundation',
        'name': 'Green Future Foundation',
        'area': 'Environmental Conservation',
        'location': {'lat': 19.0760, 'lon': 72.8777}, # Mumbai
        'year_founded': 2022,
        'impact': {
            'Trees Planted': 12500,
            'Regions Covered': 'North Mumbai, Western Suburbs',
            'CO2 Reduced (Tonnes)': 500
        },
        'details': 'Focused on reforestation and urban greening projects, the Green Future Foundation has been instrumental in combating air pollution across Mumbai. They also conduct workshops in schools to promote environmental awareness.',
        'goal': {'metric': 'Trees Planted', 'target': 20000, 'current': 12500},
        'sdg': [13, 15],
        'resources_available': [
            {'name': 'Gardening Tools', 'type': 'Equipment', 'quantity': '50 sets', 'sdg': [15]},
            {'name': 'Volunteer Coordination', 'type': 'Service', 'quantity': '10 coordinators', 'sdg': [17]}
        ],
        'resources_needed': [
            {'name': 'Sapling Donations', 'type': 'Goods', 'quantity': '5000 units', 'urgency': 'High', 'sdg': [15]},
        ]
    },
    {
        'id': 2,
        'slug': 'educate-for-all',
        'name': 'Educate For All',
        'area': "Children's Education",
        'location': {'lat': 18.5204, 'lon': 73.8567}, # Pune
        'year_founded': 2023,
        'impact': {
            'Students Enrolled': 780,
            'Schools Supported': 15,
            'Literacy Rate Improvement (%)': 12
        },
        'details': 'Educate For All provides underprivileged children with access to quality education, school supplies, and mid-day meals. Their volunteer-led tutoring programs have shown remarkable success.',
        'goal': {'metric': 'Students Enrolled', 'target': 1000, 'current': 780},
        'sdg': [4, 10],
        'resources_available': [
            {'name': 'Textbooks (Primary)', 'type': 'Goods', 'quantity': '2000 units', 'sdg': [4]},
        ],
        'resources_needed': [
            {'name': 'Volunteer Tutors', 'type': 'Volunteers', 'quantity': '50 individuals', 'urgency': 'Medium', 'sdg': [4]},
            {'name': 'Digital Tablets', 'type': 'Equipment', 'quantity': '100 units', 'urgency': 'High', 'sdg': [4, 10]}
        ]
    },
    {
        'id': 3,
        'slug': 'healthbridge-initiative',
        'name': 'HealthBridge Initiative',
        'area': 'Community Health',
        'location': {'lat': 19.2183, 'lon': 72.9781}, # Thane
        'year_founded': 2022,
        'impact': {
            'Medical Camps Held': 52,
            'Patients Treated': 21000,
            'Vaccinations Administered': 15000
        },
        'details': 'This initiative runs mobile medical camps in remote and underserved areas, providing free check-ups, essential medicines, and critical vaccinations to vulnerable populations.',
        'goal': {'metric': 'Patients Treated', 'target': 25000, 'current': 21000},
        'sdg': [3],
        'resources_available': [
            {'name': 'Mobile Medical Van', 'type': 'Equipment', 'quantity': '1 unit', 'sdg': [3]},
            {'name': 'Medical Professionals', 'type': 'Volunteers', 'quantity': '30 doctors/nurses', 'sdg': [3]}
        ],
        'resources_needed': [
            {'name': 'Basic Medicines', 'type': 'Goods', 'quantity': '500 kits', 'urgency': 'High', 'sdg': [3]},
        ]
    },
    {
        'id': 4,
        'slug': 'safe-haven-animal-rescue',
        'name': 'Safe Haven Animal Rescue',
        'area': 'Animal Welfare',
        'location': {'lat': 19.0213, 'lon': 72.8562}, # South Mumbai
        'year_founded': 2023,
        'impact': {
            'Animals Rescued': 450,
            'Successful Adoptions': 320,
            'Awareness Programs': 25
        },
        'details': 'Dedicated to rescuing and rehabilitating stray animals, Safe Haven also runs adoption drives and awareness campaigns to promote responsible pet ownership and compassion for all animals.',
        'goal': {'metric': 'Successful Adoptions', 'target': 400, 'current': 320},
        'sdg': [15],
         'resources_available': [],
        'resources_needed': [
            {'name': 'Foster Homes', 'type': 'Service', 'quantity': '20 homes', 'urgency': 'Medium', 'sdg': [15]},
            {'name': 'Animal Food', 'type': 'Goods', 'quantity': '1000 kg', 'urgency': 'High', 'sdg': [15]},
        ]
    }
]


def get_ngo_data():
    """Processes the raw data to add calculated fields like progress."""
    for ngo in ngo_impact_data:
        # Calculate goal progress percentage
        if ngo.get('goal') and ngo['goal'].get('target') > 0:
            current = ngo['goal'].get('current', 0)
            target = ngo['goal']['target']
            ngo['progress'] = round((current / target) * 100)
        else:
            ngo['progress'] = 0
    return ngo_impact_data

# --- Main Routes ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    ngos = get_ngo_data()
    selected_area = request.args.get('area', 'all')
    selected_year = request.args.get('year', 'all')

    # Create lists for filter dropdowns
    unique_areas = sorted(list(set(ngo['area'] for ngo in ngos)))
    unique_years = sorted(list(set(ngo['year_founded'] for ngo in ngos)))

    # Apply filters
    if selected_area != 'all':
        ngos = [ngo for ngo in ngos if ngo['area'] == selected_area]
    if selected_year != 'all':
        ngos = [ngo for ngo in ngos if ngo['year_founded'] == int(selected_year)]

    return render_template(
        'dashboard.html',
        ngos=ngos,
        unique_areas=unique_areas,
        unique_years=unique_years,
        selected_area=selected_area,
        selected_year=selected_year
    )

@app.route('/ngo/<slug>')
def ngo_profile(slug):
    all_ngos = get_ngo_data()
    ngo = next((n for n in all_ngos if n['slug'] == slug), None)
    if ngo:
        return render_template('ngo_profile.html', ngo=ngo)
    return "NGO not found", 404

# --- Resource Network Routes ---
@app.route('/resources')
def resource_network():
    ngos = get_ngo_data()
    selected_type = request.args.get('type', 'all')
    selected_sdg_str = request.args.get('sdg', 'all')

    all_resources = []
    for ngo in ngos:
        if ngo.get('resources_needed'):
            all_resources.extend(ngo['resources_needed'])
        if ngo.get('resources_available'):
            all_resources.extend(ngo['resources_available'])

    unique_types = sorted(list(set(r['type'] for r in all_resources)))
    unique_sdgs = sorted(list(set(sdg for r in all_resources for sdg in r['sdg'])))

    # Filter NGOs based on their resources
    filtered_ngos = []
    for ngo in ngos:
        ngo_copy = dict(ngo)
        
        needed = ngo_copy.get('resources_needed', [])
        available = ngo_copy.get('resources_available', [])

        if selected_type != 'all':
            needed = [r for r in needed if r['type'] == selected_type]
            available = [r for r in available if r['type'] == selected_type]

        if selected_sdg_str != 'all':
            selected_sdg = int(selected_sdg_str)
            needed = [r for r in needed if selected_sdg in r['sdg']]
            available = [r for r in available if selected_sdg in r['sdg']]
        
        if needed or available:
            ngo_copy['resources_needed'] = needed
            ngo_copy['resources_available'] = available
            filtered_ngos.append(ngo_copy)


    return render_template(
        'resources.html', 
        ngos=filtered_ngos,
        unique_types=unique_types,
        unique_sdgs=unique_sdgs,
        selected_type=selected_type,
        selected_sdg=selected_sdg_str
    )

@app.route('/request_resource/<int:ngo_id>/<resource_name>')
def request_resource(ngo_id, resource_name):
    all_ngos = get_ngo_data()
    ngo = next((n for n in all_ngos if n['id'] == ngo_id), None)
    if ngo:
        flash(f"Your request for '{resource_name}' from '{ngo['name']}' has been logged.", 'success')
    else:
        flash("Could not find the specified NGO.", 'danger')
    return redirect(url_for('resource_network'))

@app.route('/donate', methods=['GET', 'POST'])
def donate_resource():
    if request.method == 'POST':
        # This is where you handle the form submission from donate.html
        # In a real app, this would save to a database.
        donor_name = request.form.get('donor_name')
        email = request.form.get('email')
        resource_name = request.form.get('resource_name')
        quantity = request.form.get('quantity')
        # You can access the other form fields here as well
        
        flash(f"Thank you, {donor_name}! Your generous offer to donate '{resource_name} ({quantity})' has been received.", 'success')
        return redirect(url_for('resource_network'))
    
    # This handles the GET request, showing the form page
    return render_template('donate.html')


# --- Data Export ---
@app.route('/export-csv')
def export_csv():
    ngos = get_ngo_data()
    # Prepare data for CSV
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow(['NGO Name', 'Area of Impact', 'Year Founded', 'Goal Metric', 'Goal Target', 'Current Progress', 'Progress (%)', 'Aligned SDGs'])
    
    # Rows
    for ngo in ngos:
        sdg_str = ', '.join([str(s) for s in ngo.get('sdg', [])])
        writer.writerow([
            ngo['name'],
            ngo['area'],
            ngo['year_founded'],
            ngo['goal']['metric'],
            ngo['goal']['target'],
            ngo['goal']['current'],
            ngo['progress'],
            sdg_str
        ])
    
    output.seek(0)
    
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=ngo_impact_report.csv"}
    )


# --- Error Handling ---
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)

