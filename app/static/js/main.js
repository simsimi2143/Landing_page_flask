// static/js/main.js

// Variable global para el mapa
let map = null;

// --- INICIALIZAR EL WIDGET DE CLIMA ---
function initWeather() {
    const weatherDiv = document.getElementById('weather');
    if (weatherDiv) {
        const city = 'freire';
        const apiKey2 = 'a48ba7d6675d63364b8da518b06d1c4e';
        const url = `https://api.openweathermap.org/data/2.5/forecast?q=${city}&units=metric&appid=${apiKey2}`;

        async function getWeather() {
            try {
                const response = await fetch(url);
                if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
                const data = await response.json();
                displayWeather(data);
            } catch (error) {
                console.error("Error fetching weather data:", error);
                weatherDiv.innerHTML = '<p class="text-danger">No se pudo cargar el clima.</p>';
            }
        }

        function displayWeather(data) {
            weatherDiv.innerHTML = '';
            const dailyForecasts = {};
            
            // Procesar datos para obtener un pronóstico por día
            data.list.forEach(item => {
                const date = new Date(item.dt * 1000);
                const dateKey = date.toLocaleDateString('es-ES');
                const hour = date.getHours();
                
                // Usar el pronóstico más cercano al mediodía
                if (!dailyForecasts[dateKey] || Math.abs(hour - 12) < Math.abs(dailyForecasts[dateKey].hour - 12)) {
                    dailyForecasts[dateKey] = { 
                        ...item, 
                        hour: hour, 
                        date: date,
                        temp_max: item.main.temp_max,
                        temp_min: item.main.temp_min
                    };
                }
            });

            // Obtener los próximos 7 días
            const forecasts = Object.values(dailyForecasts).slice(0, 7);

            forecasts.forEach((day, index) => {
                const date = day.date;
                const dayName = date.toLocaleDateString('es-ES', { weekday: 'short' });
                const dayNum = date.getDate();
                const month = date.toLocaleDateString('es-ES', { month: 'short' });
                const tempMax = Math.round(day.main.temp_max);
                const tempMin = Math.round(day.main.temp_min);
                const iconCode = day.weather[0].icon;
                const isToday = index === 0;
                const cardClass = isToday ? 'day-card today' : 'day-card';

                weatherDiv.innerHTML += `
                    <div class="${cardClass}">
                        <div class="day-header">
                            <div class="day-name">${isToday ? 'Hoy' : dayName.toUpperCase()}</div>
                            <div class="day-date">${dayNum} ${month}</div>
                        </div>
                        <div class="weather-icon">
                            <img src="https://openweathermap.org/img/wn/${iconCode}@2x.png" alt="${day.weather[0].description}">
                        </div>
                        <div class="temperature">
                            <span class="temp-max">${tempMax}°</span> / 
                            <span class="temp-min">${tempMin}°</span>
                        </div>
                    </div>
                `;
            });
        }
        
        getWeather();
    }
}

// --- INICIALIZAR EL MAPA DE LEAFLET ---
function initMap() {
    const mapDiv = document.getElementById('map');
    if (mapDiv && !mapDiv.classList.contains('leaflet-container')) {
        // Limpiar el contenedor del mapa
        mapDiv.innerHTML = '';
        
        // Crear nuevo mapa
        map = L.map('map').setView([-38.9515, -72.6293], 15);
        
        // Agregar capa de tiles
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            maxZoom: 18
        }).addTo(map);
        
        // Agregar marcador
        L.marker([-38.9515, -72.6293]).addTo(map)
            .bindPopup(`
                <div style="text-align: center;">
                    <strong>Municipalidad de Freire</strong><br>
                    <small>Click para cerrar</small>
                </div>
            `)
            .openPopup();
        
        // Forzar redimensionamiento después de un delay
        setTimeout(() => {
            if (map) {
                map.invalidateSize();
            }
        }, 100);
    }
}

// --- REDIMENSIONAR MAPA CUANDO CAMBIA EL TAMAÑO DE PANTALLA ---
function handleMapResize() {
    if (map) {
        setTimeout(() => {
            map.invalidateSize();
            // Re-centrar el mapa después del redimensionamiento
            map.setView([-38.9515, -72.6293], map.getZoom());
        }, 300);
    }
}

// --- LÓGICA MEJORADA PARA EXPANDIR/CONTRAER NOTICIAS ---
function initNewsExpand() {
    const mainCarousel = document.getElementById('mainCarousel');
    if (mainCarousel) {
        mainCarousel.addEventListener('click', function(event) {
            const target = event.target;
            
            if (target.classList.contains('see-more-btn')) {
                event.preventDefault();
                event.stopPropagation();
                
                const caption = target.closest('.carousel-caption');
                if (caption) {
                    caption.classList.add('expanded');
                }
            }
            
            if (target.classList.contains('see-less-btn')) {
                event.preventDefault();
                event.stopPropagation();
                
                const caption = target.closest('.carousel-caption');
                if (caption) {
                    caption.classList.remove('expanded');
                }
            }
        });

        // Cerrar noticias expandidas al cambiar de slide
        mainCarousel.addEventListener('slide.bs.carousel', function() {
            const expandedCaptions = document.querySelectorAll('.carousel-caption.expanded');
            expandedCaptions.forEach(caption => {
                caption.classList.remove('expanded');
            });
        });
    }
}

// --- INICIALIZAR TODO CUANDO EL DOCUMENTO ESTÉ LISTO ---
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar componentes
    initWeather();
    initMap();
    initNewsExpand();
    
    // Redimensionar mapa cuando cambia el tamaño de la ventana
    window.addEventListener('resize', handleMapResize);
    
    // Redimensionar mapa cuando se cambia de pestaña (para navegadores móviles)
    document.addEventListener('visibilitychange', function() {
        if (!document.hidden) {
            setTimeout(handleMapResize, 500);
        }
    });
});

// --- FUNCIÓN PARA DESTRUIR EL MAPA (útil si necesitas reiniciarlo) ---
function destroyMap() {
    if (map) {
        map.remove();
        map = null;
    }
}