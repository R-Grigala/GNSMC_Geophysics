document.addEventListener("DOMContentLoaded", function() {
    const projectId = document.getElementById("projectId").getAttribute("data-project-id");
    const carouselInner = document.getElementById('carouselInner');
    const carouselIndicators = document.getElementById('carouselIndicators');

    // Fetch and display images when the DOM is fully loaded
    fetchImages();

    function fetchImages() {
        fetch(`/api/project/${projectId}/images`)
            .then(response => response.json())
            .then(data => {
                if (Array.isArray(data) && data.length > 0) {
                    populateCarousel(data);
                } else {
                    displayPlaceholderImage();
                }
            })
            .catch(handleError);
    }

    function populateCarousel(images) {
        carouselInner.innerHTML = '';
        carouselIndicators.innerHTML = '';

        images.forEach((image, index) => {
            const item = createCarouselItem(image.path, image.id, index);
            carouselInner.appendChild(item);

            const indicator = createIndicator(index);
            carouselIndicators.appendChild(indicator);
        });
    }

    function createCarouselItem(imagePath, imageId, index) {
        const item = document.createElement('div');
        item.className = `carousel-item imageProjectDiv${index === 0 ? ' active' : ''}`;
        item.setAttribute('data-slide-to', index);

        const img = createImageElement(`/images/${projectId}/${imagePath}`);
        const deleteButton = createDeleteButton(imageId, item);

        item.appendChild(img);
        item.appendChild(deleteButton);
        return item;
    }

    function createImageElement(src) {
        const img = document.createElement('img');
        img.src = src;
        img.alt = 'Project Image';
        img.style.width = '100%';
        img.style.height = '100%';
        img.style.objectFit = 'cover';
        img.onerror = () => img.src = '/static/img/image_not_available.png';
        return img;
    }

    function createDeleteButton(imageId, carouselItem) {
        const deleteButton = document.createElement('button');
        deleteButton.className = 'btn btn-sm btn-danger delete-btn';
        deleteButton.innerHTML = 'წაშლა';
        deleteButton.style.position = 'absolute';
        deleteButton.style.top = '10px';
        deleteButton.style.right = '150px';
        deleteButton.onclick = () => deleteImage(projectId, imageId, carouselItem);
        return deleteButton;
    }

    function createIndicator(index) {
        const indicator = document.createElement('button');
        indicator.type = 'button';
        indicator.setAttribute('data-bs-target', '#carouselExampleIndicators');
        indicator.setAttribute('data-bs-slide-to', index);
        indicator.className = index === 0 ? 'active' : '';
        indicator.setAttribute('aria-current', index === 0 ? 'true' : 'false');
        indicator.setAttribute('aria-label', `Slide ${index + 1}`);
        return indicator;
    }

    function deleteImage(projectId, imageId) {
        if (!confirm('დარწმუნებული ხართ რომ გსურთ ამ სურათის წაშლა?')) return;

        fetch(`/api/project/${projectId}/images/${imageId}`, {
            method: 'DELETE',
        })
        .then(response => {
            if (response.ok) {
                alert('წარმატებით წაიშალა');
                fetchImages(); // Refresh carousel dynamically
            } else {
                handleError(new Error('Error deleting image'));
            }
        })
        .catch(handleError);
    }

    document.getElementById('uploadButton').onclick = function() {
        uploadImages();
    };

    function uploadImages() {
        const inputElement = document.getElementById('images');
        const files = inputElement.files;

        if (files.length === 0) {
            alert('გთხოვთ აირჩიოთ სურათები');
            return;
        }

        const formData = new FormData();
        for (let i = 0; i < files.length; i++) {
            formData.append('images', files[i]);
        }

        fetch(`/api/project/${projectId}/images`, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json().then(data => ({
            status: response.status,
            body: data
        })))
        .then(({ status, body }) => {
            if (status === 200) {
                inputElement.value = '';
                alert('წარმატებით აიტვირთა');
                fetchImages(); // Refresh carousel dynamically
            } else {
                alert(body.message || 'Error სურათების ატვირთვისას მოხდა შეცდომა');
            }
        })
        .catch(handleError);
    }

    function displayPlaceholderImage() {
        carouselInner.innerHTML = ''; // Clear existing images
        const item = document.createElement('div');
        item.className = `carousel-item imageProjectDiv active`;
        item.setAttribute('data-slide-to', 0);

        const img = createImageElement('/static/img/image_not_available.png');

        item.appendChild(img);
        carouselInner.appendChild(item);
    }

    function handleError(error) {
        console.error('Error:', error);
        alert('ოპერაციის დროს შეცდომა მოხდა');
    }
});
