import csv
from io import StringIO
from flask import Flask, render_template, request, Response
from datetime import datetime

app = Flask(__name__)

# --- Expanded Local Data ---
ngo_impact_data = [
    {
        'id': 1,
        'slug': 'green-future-foundation',
        'name': 'Green Future Foundation',
        'area': 'Environmental Conservation',
        'location': {'lat': 19.0760, 'lon': 72.8777},
        'start_date': '2022-01-15',
        'impact': {
            'Trees Planted': 12500,
            'Regions Covered': 'North Mumbai, Western Suburbs',
            'CO2 Reduced (Tonnes)': 500
        },
        'details': 'Focused on reforestation and urban greening projects, the Green Future Foundation has been instrumental in combating air pollution across Mumbai. They also conduct workshops in schools to promote environmental awareness.',
        'goal': {'metric': 'Trees Planted', 'target': 20000},
        'sdg': [13, 15] # Climate Action, Life on Land
    },
    {
        'id': 2,
        'slug': 'educate-for-all',
        'name': 'Educate For All',
        'area': "Children's Education",
        'location': {'lat': 18.5204, 'lon': 73.8567},
        'start_date': '2023-06-20',
        'impact': {
            'Students Enrolled': 780,
            'Schools Supported': 15,
            'Literacy Rate Improvement': '12%'
        },
        'details': 'Educate For All provides underprivileged children with access to quality education, school supplies, and mid-day meals. Their volunteer-led tutoring programs have shown remarkable success.',
        'goal': {'metric': 'Students Enrolled', 'target': 1000},
        'sdg': [4] # Quality Education
    },
    {
        'id': 3,
        'slug': 'healthbridge-initiative',
        'name': 'HealthBridge Initiative',
        'area': 'Community Health',
        'location': {'lat': 19.2183, 'lon': 72.9781},
        'start_date': '2022-11-01',
        'impact': {
            'Medical Camps Held': 52,
            'Patients Treated': 21000,
            'Vaccinations Administered': 15000
        },
        'details': 'This initiative runs mobile medical camps in remote and underserved areas, providing free check-ups, essential medicines, and critical vaccinations to vulnerable populations.',
        'goal': {'metric': 'Patients Treated', 'target': 25000},
        'sdg': [3] # Good Health and Well-being
    },
    {
        'id': 4,
        'slug': 'safe-haven-animal-rescue',
        'name': 'Safe Haven Animal Rescue',
        'area': 'Animal Welfare',
        'location': {'lat': 19.0213, 'lon': 72.8562},
        'start_date': '2023-02-10',
        'impact': {
            'Animals Rescued': 450,
            'Successful Adoptions': 320,
            'Community Awareness Programs': 25
        },
        'details': 'Dedicated to rescuing and rehabilitating stray animals, Safe Haven also runs adoption drives and awareness campaigns to promote responsible pet ownership and compassion for all animals.',
        'goal': {'metric': 'Successful Adoptions', 'target': 400},
        'sdg': [15] # Life on Land
    }
]

# --- Helper function to add progress to data ---
def get_processed_ngo_data():
    """Processes the raw data to calculate progress and add year."""
    processed_data = []
    for ngo in ngo_impact_data:
        # Calculate progress
        goal_metric = ngo['goal']['metric']
        if goal_metric in ngo['impact']:
            current_value = ngo['impact'][goal_metric]
            target_value = ngo['goal']['target']
            progress = round((current_value / target_value) * 100) if target_value > 0 else 0
            ngo['progress'] = progress
        else:
            ngo['progress'] = 0

        # Extract year for filtering
        ngo['year_founded'] = datetime.strptime(ngo['start_date'], '%Y-%m-%d').year
        processed_data.append(ngo)
    return processed_data


# --- App Routes ---

@app.route('/')
def home():
    """Main Home Page"""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """Impact Measurement Dashboard Page"""
    all_ngos = get_processed_ngo_data()

    selected_area = request.args.get('area', 'all')
    selected_year = request.args.get('year', 'all')

    filtered_ngos = all_ngos
    if selected_area != 'all':
        filtered_ngos = [ngo for ngo in filtered_ngos if ngo['area'] == selected_area]
    if selected_year != 'all':
        filtered_ngos = [ngo for ngo in filtered_ngos if str(ngo.get('year_founded', '')) == selected_year]

    unique_areas = sorted(list(set(ngo['area'] for ngo in all_ngos)))
    unique_years = sorted(list(set(str(ngo.get('year_founded', '')) for ngo in all_ngos if 'year_founded' in ngo)), reverse=True)

    return render_template(
        'dashboard.html',
        ngos=filtered_ngos,
        unique_areas=unique_areas,
        unique_years=unique_years,
        selected_area=selected_area,
        selected_year=selected_year
    )

@app.route('/ngo/<slug>')
def ngo_profile(slug):
    """Detailed profile page for a single NGO."""
    all_ngos = get_processed_ngo_data()
    ngo = next((n for n in all_ngos if n['slug'] == slug), None)
    if ngo:
        return render_template('ngo_profile.html', ngo=ngo)
    return "NGO not found", 404

@app.route('/export-csv')
def export_csv():
    """Exports the current NGO data to a CSV file."""
    all_ngos = get_processed_ngo_data()
    
    si = StringIO()
    # Expanded fieldnames to reflect new data structure
    fieldnames = ['name', 'area', 'year_founded', 'progress', 'goal_metric', 'goal_target']
    writer = csv.writer(si)
    
    writer.writerow(fieldnames)
    
    for ngo in all_ngos:
        writer.writerow([
            ngo.get('name'),
            ngo.get('area'),
            ngo.get('year_founded'),
            f"{ngo.get('progress', 0)}%",
            ngo.get('goal', {}).get('metric'),
            ngo.get('goal', {}).get('target')
        ])
    
    output = si.getvalue()
    
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=ngo_impact_report.csv"}
    )
    
# --- Other Pages ---

@app.route('/resources')
def resource_network():
    """Community Resource Sharing Network Page"""
    return render_template('resources.html')

@app.route('/data')
def data_collection():
    """Field Data Collection App Page"""
    return render_template('data.html')

# --- Run the App ---
if __name__ == '__main__':
    app.run(debug=True)

