    const map = new maplibregl.Map({
        container: 'map',
        style: 'https://api.maptiler.com/maps/streets/style.json?key=get_your_own_OpIi9ZULNHzrESv6T2vL',
        center: [0, 0],
        zoom: 1,
        maplibreLogo: true
    });

    map.on('click', function (e) {
    const lat = e.lngLat.lat.toFixed(6);
    const lon = e.lngLat.lng.toFixed(6);
    document.getElementById("latInput").value = lat;
    document.getElementById("lonInput").value = lon;
    });

    function flyToCountry() {
        const country = document.getElementById("countryInput").value;
        if (!country) {
            alert("Please enter a country name.");
            return;
        }

        fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(country)}`)
            .then(response => response.json())
            .then(data => {
                if (data.length === 0) {
                    alert("Country not found.");
                    return;
                }
                const lat = parseFloat(data[0].lat);
                const lon = parseFloat(data[0].lon);
                map.flyTo({ center: [lon, lat], zoom: 6 });
                document.getElementById("latInput").value = lat.toFixed(6);
                document.getElementById("lonInput").value = lon.toFixed(6);
            })
            .catch(error => {
                console.error("Error fetching country coordinates:", error);
                alert("Failed to locate country.");
            });
    }

    function goToLocation() {
        const lat = parseFloat(document.getElementById("latInput").value);
        const lon = parseFloat(document.getElementById("lonInput").value);
        if (!isNaN(lat) && !isNaN(lon)) {
            map.flyTo({ center: [lon, lat], zoom: 8 });
        } else {
            alert("Please enter valid latitude and longitude.");
        }
    }

    function submitEnvironmentalData() {
        const lat = parseFloat(document.getElementById("latInput").value);
        const lon = parseFloat(document.getElementById("lonInput").value);
        const alt = parseFloat(document.getElementById("altInput").value);
        const area = parseFloat(document.getElementById("areaInput").value);

        if (isNaN(lat) || isNaN(lon) || isNaN(alt) || isNaN(area)) {
            alert("Please enter all values correctly.");
            return;
        }

        fetch("/recommend", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ lat, lon, alt, area })
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById("recommendationResult").innerText = data.recommendation;
        })
        .catch(error => {
            console.error("Error:", error);
            alert("Something went wrong.");
        });
    }
    function closeModal() {
        document.getElementById("introModal").style.display = "none";
        localStorage.setItem("intro_shown", "true");
    }

    window.onload = function () {
        if (!localStorage.getItem("intro_shown")) {
            document.getElementById("introModal").style.display = "flex";
        }
    };
    function toggleLocationMethod() {
    const useCountry = document.getElementById("useCountry").checked;
    document.getElementById("countryInputGroup").style.display = useCountry ? "block" : "none";
    document.getElementById("coordInputGroup").style.display = useCountry ? "none" : "block";
    }