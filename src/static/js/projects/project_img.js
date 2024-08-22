document.addEventListener("DOMContentLoaded", function() {
    const projectIdElement = document.getElementById("projectId");
    const projectId = projectIdElement.getAttribute("data-project-id");
    const carouselInner = document.getElementById('carouselInner');
    const carouselIndicators = document.getElementById('carouselIndicators');

    fetch(`/api/project/${projectId}/images`)
        .then(response => {
            console.log("API response status:", response.status);
            return response.json();
        })
        .then(data => {
            console.log("API response data:", data);

            if (!Array.isArray(data) || data.length === 0) {
                console.log('No images found or invalid data format');
                return;
            }

            data.forEach((image, index) => {
                // Create a carousel item
                const item = document.createElement('div');
                item.className = 'carousel-item imageProjectDiv' + (index === 0 ? ' active' : '');
                item.setAttribute('data-slide-to', index);

                const img = document.createElement('img');
                img.src = `/images/${projectId}/${image.path}`;
                img.alt = 'Project Image';
                img.style.width = '100%';
                img.style.height = '100%';
                img.style.objectFit = 'cover';

                // Create a delete button
                const deleteButton = document.createElement('button');
                deleteButton.className = 'btn btn-sm btn-danger delete-btn';
                deleteButton.innerHTML = 'წაშლა';
                deleteButton.style.position = 'absolute';
                deleteButton.style.top = '10px';
                deleteButton.style.right = '150px';
                deleteButton.addEventListener('click', function() {
                    deleteImage(projectId, image.id, item);
                });

                item.appendChild(img);
                item.appendChild(deleteButton);
                carouselInner.appendChild(item);

                // Create an indicator
                const indicator = document.createElement('button');
                indicator.type = 'button';
                indicator.setAttribute('data-bs-target', '#carouselExampleIndicators');
                indicator.setAttribute('data-bs-slide-to', index);
                indicator.className = index === 0 ? 'active' : '';
                indicator.setAttribute('aria-current', index === 0 ? 'true' : 'false');
                indicator.setAttribute('aria-label', `Slide ${index + 1}`);
                carouselIndicators.appendChild(indicator);
            });
        })
        .catch(error => {
            console.error('Error fetching images:', error);
        });

    function deleteImage(projectId, imageId, carouselItem) {

        const confirmed = confirm('დარწმუნებული ხართ რომ გსურთ ამ სურათის წაშლა?');

        if (confirmed){
            fetch(`/api/project/${projectId}/images/${imageId}`, {
                method: 'DELETE',
            })
            .then(response => {
                if (response.ok) {
                    const nextItem = carouselItem.nextElementSibling || carouselItem.previousElementSibling;
                    if (nextItem) {
                        const nextIndex = nextItem.getAttribute('data-slide-to');
                        const carouselElement = document.querySelector('#carouselExampleIndicators');
                        const carouselInstance = bootstrap.Carousel.getInstance(carouselElement);
                        carouselInstance.to(nextIndex); // Move to the next/prev slide before deleting
                    }
    
                    const indicatorIndex = Array.from(carouselItem.parentNode.children).indexOf(carouselItem);
                    carouselItem.remove();
                    carouselIndicators.children[indicatorIndex].remove();
                    console.log('Image deleted successfully');
                } else {
                    console.error('Error deleting image:', response.statusText);
                }
            })
            .catch(error => {
                console.error('Error deleting image:', error);
            });
        }
    }
    

});
