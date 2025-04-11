document.addEventListener('DOMContentLoaded', function() {
    // Plant database search and filtering
    setupPlantDatabase();
    
    // Contact form validation
    setupContactForm();
    
    // Plant detail modal handlers
    setupPlantModals();
});

function setupPlantDatabase() {
    const plantSearch = document.getElementById('plantSearch');
    const categoryFilter = document.getElementById('categoryFilter');
    const conditionFilter = document.getElementById('conditionFilter');
    const plantList = document.getElementById('plantList');
    const pagination = document.getElementById('pagination');
    
    if (!plantSearch || !categoryFilter || !conditionFilter || !plantList) {
        return; // Skip if we're not on the database page
    }
    
    let currentPage = 1;
    
    // Load plants on page load
    loadPlants();
    
    // Setup event listeners
    plantSearch.addEventListener('input', debounce(function() {
        currentPage = 1;
        loadPlants();
    }, 500));
    
    categoryFilter.addEventListener('change', function() {
        currentPage = 1;
        loadPlants();
    });
    
    conditionFilter.addEventListener('change', function() {
        currentPage = 1;
        loadPlants();
    });
    
    // Handle pagination clicks
    if (pagination) {
        pagination.addEventListener('click', function(e) {
            if (e.target.classList.contains('page-link')) {
                e.preventDefault();
                
                if (e.target.textContent === 'Previous') {
                    if (currentPage > 1) currentPage--;
                } else if (e.target.textContent === 'Next') {
                    currentPage++;
                } else {
                    currentPage = parseInt(e.target.textContent);
                }
                
                loadPlants();
            }
        });
    }
    
    function loadPlants() {
        const search = plantSearch.value;
        const category = categoryFilter.value;
        const condition = conditionFilter.value;
        
        // Show loading state
        plantList.innerHTML = '<div class="col-12 text-center"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div></div>';
        
        // Fetch plants from API
        fetch(`/api/plants?search=${encodeURIComponent(search)}&category=${encodeURIComponent(category)}&condition=${encodeURIComponent(condition)}&page=${currentPage}`)
            .then(response => response.json())
            .then(data => {
                displayPlants(data);
                updatePagination(data);
            })
            .catch(error => {
                console.error('Error fetching plants:', error);
                plantList.innerHTML = '<div class="col-12 alert alert-danger">Error loading plants. Please try again later.</div>';
            });
    }
    
    function displayPlants(data) {
        if (data.plants.length === 0) {
            plantList.innerHTML = '<div class="col-12 alert alert-info">No plants found matching your criteria. Try adjusting your filters.</div>';
            return;
        }
        
        let html = '';
        data.plants.forEach(plant => {
            let conditionBadges = '';
            plant.conditions.forEach(condition => {
                conditionBadges += `<span class="badge medicine-badge">${condition}</span>`;
            });
            
            html += `
                <div class="col-lg-3 col-md-4 col-sm-6 mb-4">
                    <div class="plant-card plant-list-card" onclick="window.location.href='/plant/${plant.id}'">
                        <img src="/static/uploads/${plant.image || 'placeholder.jpg'}" class="plant-img w-100" alt="${plant.name}">
                        <div class="p-3">
                            <h4>${plant.name}</h4>
                            <p class="text-muted">${plant.scientific_name}</p>
                            <p class="small">${plant.description.substring(0, 100)}${plant.description.length > 100 ? '...' : ''}</p>
                            <div>
                                ${conditionBadges}
                            </div>
                        </div>
                    </div>
                </div>
            `;
        });
        
        plantList.innerHTML = html;
    }
    
    function updatePagination(data) {
        if (!pagination) return;
        
        const totalPages = data.pages;
        let html = `
            <nav aria-label="Page navigation">
                <ul class="pagination justify-content-center">
                    <li class="page-item ${currentPage === 1 ? 'disabled' : ''}">
                        <a class="page-link" href="#" tabindex="-1">Previous</a>
                    </li>
        `;
        
        for (let i = 1; i <= totalPages; i++) {
            html += `<li class="page-item ${i === currentPage ? 'active' : ''}"><a class="page-link" href="#">${i}</a></li>`;
        }
        
        html += `
                    <li class="page-item ${currentPage === totalPages ? 'disabled' : ''}">
                        <a class="page-link" href="#">Next</a>
                    </li>
                </ul>
            </nav>
        `;
        
        pagination.innerHTML = html;
    }
}

function setupContactForm() {
    const contactForm = document.getElementById('contactForm');
    
    if (!contactForm) return;
    
    contactForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Basic validation
        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const message = document.getElementById('message').value;
        
        if (!name || !email || !message) {
            alert('Please fill in all required fields.');
            return;
        }
        
        // Email validation
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            alert('Please enter a valid email address.');
            return;
        }
        
        // Submit the form
        contactForm.submit();
    });
}

function setupPlantModals() {
    // Setup click handlers for "Learn More" buttons
    const learnMoreButtons = document.querySelectorAll('[data-plant]');
    
    learnMoreButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const plantName = this.getAttribute('data-plant');
            
            // In a real application, you would fetch plant details from the server
            // For now, we'll just show a simple alert
            alert(`You clicked to learn more about ${plantName}. In a complete implementation, this would open a modal with detailed information.`);
            
            // Example of how you might fetch and display plant details:
            /*
            fetch(`/api/plant/${plantName}`)
                .then(response => response.json())
                .then(data => {
                    // Populate and show modal with plant details
                    const modal = new bootstrap.Modal(document.getElementById('plantModal'));
                    document.getElementById('modalPlantTitle').textContent = data.name;
                    // Set other modal content...
                    modal.show();
                });
            */
        });
    });
}

// Utility function for debouncing
function debounce(func, wait) {
    let timeout;
    return function() {
        const context = this;
        const args = arguments;
        clearTimeout(timeout);
        timeout = setTimeout(() => {
            func.apply(context, args);
        }, wait);
    };
}