# DealHopper

DealHopper is a smartphone price comparator designed to help users find the best deals across multiple online stores, such as PcComponentes, MediaMarkt, and PhoneHouse. With its intuitive interface and powerful features, DealHopper simplifies the process of price comparison and recommendation.

## Technologies Used
DealHopper is built using the following tools and frameworks:
- **Django**: Backend framework for managing the web application.
- **BeautifulSoup**: For scraping smartphone prices and details from online stores.
- **Whoosh**: For implementing an efficient search index.
- **Recommendation System (RS)**: Provides personalized recommendations based on user preferences.

## Installation
Follow these steps to set up and run DealHopper on your local machine:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/DealHopper.git
   cd DealHopper
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create and apply the migrations
   ```bash
      python manage.py makemigrations
      python manage.py migrate
   ```

## Run the Server
1. Start the development server:
   ```bash
   python manage.py runserver
   ```

2. Open your web browser and navigate to `http://127.0.0.1:7777`.

3. Enjoy exploring and comparing smartphone prices effortlessly!

