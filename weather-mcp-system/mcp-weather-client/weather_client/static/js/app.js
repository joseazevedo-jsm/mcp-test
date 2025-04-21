// DOM Elements
const locationInput = document.getElementById('location-input');
const searchButton = document.getElementById('search-button');
const locationsDropdown = document.getElementById('locations-dropdown');
const locationsList = document.getElementById('locations-list');
const loadingIndicator = document.getElementById('loading-indicator');
const weatherContainer = document.getElementById('weather-container');
const errorContainer = document.getElementById('error-container');
const errorMessage = document.getElementById('error-message');
const rawDataElement = document.getElementById('raw-data');
const rawDataContent = document.getElementById('raw-data-content');

// Weather display elements
const weatherLocation = document.getElementById('weather-location');
const weatherDate = document.getElementById('weather-date');
const temperature = document.getElementById('temperature');
const conditions = document.getElementById('conditions');
const humidity = document.getElementById('humidity');
const windSpeed = document.getElementById('wind-speed');
const forecast = document.getElementById('forecast');

// Initialize date
weatherDate.textContent = new Date().toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
});

// Event Listeners
document.addEventListener('DOMContentLoaded', fetchLocations);
searchButton.addEventListener('click', handleSearch);
locationInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        handleSearch();
    }
});

// Show/hide locations dropdown based on input focus
locationInput.addEventListener('focus', () => {
    if (locationsList.children.length > 0) {
        locationsDropdown.style.display = 'block';
    }
});

document.addEventListener('click', (e) => {
    if (!locationsDropdown.contains(e.target) && e.target !== locationInput) {
        locationsDropdown.style.display = 'none';
    }
});

// Functions
/**
 * Handle the search button click
 */
function handleSearch() {
    const location = locationInput.value.trim();
    if (location) {
        fetchWeather(location);
    } else {
        showError('Please enter a location');
    }
}

/**
 * Fetch available locations from the API
 */
async function fetchLocations() {
    try {
        const response = await fetch('/api/locations');
        const data = await response.json();
        
        if (data.locations && Array.isArray(data.locations)) {
            populateLocationsDropdown(data.locations);
        }
    } catch (error) {
        console.error('Error fetching locations:', error);
    }
}

/**
 * Populate the locations dropdown
 */
function populateLocationsDropdown(locations) {
    locationsList.innerHTML = '';
    
    if (locations.length === 0) {
        return;
    }
    
    locations.forEach(location => {
        if (typeof location === 'string') {
            const li = document.createElement('li');
            li.textContent = location;
            li.addEventListener('click', () => {
                locationInput.value = location;
                locationsDropdown.style.display = 'none';
                fetchWeather(location);
            });
            locationsList.appendChild(li);
        }
    });
}

/**
 * Fetch weather data for a location
 */
async function fetchWeather(location) {
    // Show loading indicator
    showLoading();
    
    try {
        const response = await fetch(`/api/weather?location=${encodeURIComponent(location)}`);
        const data = await response.json();
        
        if (data.error) {
            showError(data.error);
            return;
        }
        
        // Display the raw data
        rawDataContent.textContent = data.data;
        rawDataElement.style.display = 'block';
        
        // Parse and display the weather data
        displayWeatherData(data.data, location);
        
        // Hide loading indicator and show weather container
        hideLoading();
        weatherContainer.style.display = 'block';
        errorContainer.style.display = 'none';
    } catch (error) {
        hideLoading();
        showError('Failed to fetch weather data. Please try again.');
        console.error('Error:', error);
    }
}

/**
 * Display the weather data on the page
 */
function displayWeatherData(weatherText, searchLocation) {
    // Parse the weather text
    const lines = weatherText.split('\n');
    
    // Extract location from the first line
    const locationMatch = lines[0].match(/Weather for (.+):/);
    if (locationMatch && locationMatch[1]) {
        weatherLocation.textContent = locationMatch[1];
    } else {
        weatherLocation.textContent = searchLocation;
    }
    
    // Extract temperature
    const tempMatch = lines.find(line => line.includes('Temperature:'));
    if (tempMatch) {
        const temp = tempMatch.split('Temperature: ')[1];
        temperature.textContent = temp;
    } else {
        temperature.textContent = 'N/A';
    }
    
    // Extract conditions
    const condMatch = lines.find(line => line.includes('Conditions:'));
    if (condMatch) {
        const cond = condMatch.split('Conditions: ')[1];
        conditions.textContent = cond;
    } else {
        conditions.textContent = 'Unknown';
    }
    
    // Extract humidity
    const humMatch = lines.find(line => line.includes('Humidity:'));
    if (humMatch) {
        const hum = humMatch.split('Humidity: ')[1];
        humidity.textContent = hum;
    } else {
        humidity.textContent = 'N/A';
    }
    
    // Extract wind speed
    const windMatch = lines.find(line => line.includes('Wind Speed:'));
    if (windMatch) {
        const wind = windMatch.split('Wind Speed: ')[1];
        windSpeed.textContent = wind;
    } else {
        windSpeed.textContent = 'N/A';
    }
    
    // Extract forecast
    forecast.innerHTML = '';
    const forecastStartIndex = lines.findIndex(line => line.includes('Forecast:'));
    
    if (forecastStartIndex !== -1) {
        // Process forecast lines
        const forecastLines = lines.slice(forecastStartIndex + 1).filter(line => line.trim() !== '');
        
        forecastLines.forEach(line => {
            if (line.startsWith('- ')) {
                const forecastData = line.substring(2);
                const parts = forecastData.split(':');
                
                if (parts.length >= 2) {
                    const day = parts[0].trim();
                    const details = parts[1].trim();
                    
                    // Extract conditions and temperatures
                    const condEndIndex = details.indexOf(',');
                    const dayConditions = condEndIndex !== -1 ? details.substring(0, condEndIndex).trim() : details.trim();
                    
                    let highTemp = 'N/A';
                    let lowTemp = 'N/A';
                    
                    if (condEndIndex !== -1) {
                        const tempPart = details.substring(condEndIndex + 1).trim();
                        const tempParts = tempPart.split(',');
                        
                        if (tempParts.length >= 2) {
                            highTemp = tempParts[0].replace('High:', '').trim();
                            lowTemp = tempParts[1].replace('Low:', '').trim();
                        }
                    }
                    
                    // Create forecast day element
                    const forecastDay = document.createElement('div');
                    forecastDay.className = 'forecast-day';
                    forecastDay.innerHTML = `
                        <div class="forecast-day-name">${day}</div>
                        <div class="forecast-conditions">${dayConditions}</div>
                        <div class="forecast-temp">
                            <span class="forecast-high">${highTemp}</span>
                            <span class="forecast-low">${lowTemp}</span>
                        </div>
                    `;
                    
                    forecast.appendChild(forecastDay);
                }
            }
        });
    }
}

/**
 * Show loading indicator
 */
function showLoading() {
    loadingIndicator.style.display = 'block';
    weatherContainer.style.display = 'none';
    errorContainer.style.display = 'none';
    rawDataElement.style.display = 'none';
}

/**
 * Hide loading indicator
 */
function hideLoading() {
    loadingIndicator.style.display = 'none';
}

/**
 * Show error message
 */
function showError(message) {
    errorMessage.textContent = message;
    errorContainer.style.display = 'block';
    weatherContainer.style.display = 'none';
    hideLoading();
}
