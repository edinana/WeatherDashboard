document.addEventListener('DOMContentLoaded', () => {
    const dropdown = document.getElementById('capital-select');
    const cityName = document.getElementById('city-name');
    const temperature = document.getElementById('temperature');
    const condition = document.getElementById('condition');
    const humidity = document.getElementById("humidity");
    const windSpeed = document.getElementById("wind-speed");

    fetch('https://restcountries.com/v3.1/all', { cache: "no-store" })
        .then(response => response.json())
        .then(data => {
            const capitals = data.map(country => country.capital).filter(capital => capital !== undefined);
            populateCapitalsDropdown(capitals);
        })
        .catch(error => {
            console.error('Error fetching capitals:', error);
        });

    function populateCapitalsDropdown(capitals) {
        const flatCapitals = capitals
            .flat()
            .filter(capital => typeof capital === "string");

        flatCapitals.sort((a, b) => a.localeCompare(b));

        flatCapitals.forEach(capital => {
            const option = document.createElement('option');
            option.value = capital;
            option.textContent = capital;
            dropdown.appendChild(option);
        });

        const defaultCity = "Cairo";
        dropdown.value = defaultCity;
        cityName.textContent = defaultCity;
        updateWeather(defaultCity);
    }

    dropdown.addEventListener('change', () => {
        const selectedCity = dropdown.value;
        cityName.textContent = selectedCity;
        updateWeather(selectedCity);
    });

    function updateWeather(city) {
    const apiUrl = `/weather/${city}/`;

    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            if (data) {
                const temperatureValue = Math.ceil(data.temp);
                const conditionValue = data.condition;
                const humidityValue = Math.ceil(data.humidity);
                const windValue = Math.ceil(data.wind * 2.237);

                temperature.textContent = `Temperature: ${temperatureValue}°C`;
                condition.textContent = conditionValue;
                humidity.textContent = `Humidity: ${humidityValue}%`;
                windSpeed.textContent = `Wind: ${windValue} mph`;

                setBackground(conditionValue);
            } else {
                console.error('No weather data available for this city');
            }
        })
        .catch(error => {
            console.error('Error fetching weather data:', error);
        });
    }

    function setBackground(weatherCondition) {
        const body = document.querySelector('body');

        body.classList.remove('sunny', 'rainy', 'cloudy', 'snowy');

        const condition = weatherCondition.toLowerCase();

        if (condition.includes('sun')) {
            body.classList.add('sunny');
        } else if (condition.includes('rain')) {
            body.classList.add('rainy');
        } else if (condition.includes('cloud')) {
            body.classList.add('cloudy');
        } else if (condition.includes('snow')) {
            body.classList.add('snowy');
        }
    }

    document.getElementById("forecast-button").addEventListener("click", function() {
        const city = dropdown.value;
        const temperatureValue = temperature.textContent.split(":")[1].trim().replace("°C", "");
        const conditionValue = condition.textContent;
        const humidityValue = humidity.textContent.split(":")[1].trim().replace("%", "");
        const windSpeedValue = windSpeed.textContent.split(":")[1].trim().replace("mph", "") * 0.44704;

        // generated in user session
        const csrfToken = getCookie('csrftoken');

        fetch('/forecast/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({
                city: city,
                temperature: temperatureValue,
                humidity: humidityValue,
                wind_speed: windSpeedValue,
                condition: conditionValue
            })
        })
        .then(response => response.json())
        .then(data => {
            const modal = document.getElementById('forecast-modal');
            const forecastData = document.getElementById('forecast-data');
            const closeModal = document.querySelector('.close');

            forecastData.innerHTML = `
                <p><strong>City:</strong> ${city}</p>
                <p><strong>Temperature:</strong> ${Math.round(data.forecast.forecast_temperature)}°C</p>
                <p><strong>Condition:</strong> ${data.forecast.forecast_condition}</p>
                <p><strong>Humidity:</strong> ${Math.round(data.forecast.forecast_humidity)}%</p>
                <p><strong>Wind Speed:</strong> ${Math.round(data.forecast.forecast_wind_speed * 2.23694)} mph</p>
            `;

            modal.style.display = "block";

            closeModal.onclick = function() {
                modal.style.display = "none";
            };

            window.onclick = function(event) {
                if (event.target === modal) {
                    modal.style.display = "none";
                }
            };
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});