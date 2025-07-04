document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('stego-form');
    const actionRadios = document.querySelectorAll('input[name="action"]');
    const messageGroup = document.getElementById('message-group');
    
    // Show/hide message textarea based on action
    function toggleMessageField() {
        const selectedAction = document.querySelector('input[name="action"]:checked').value;
        messageGroup.style.display = selectedAction === 'encode' ? 'block' : 'none';
    }
    
    // Initial setup
    toggleMessageField();
    
    // Add event listeners for radio buttons
    actionRadios.forEach(radio => {
        radio.addEventListener('change', toggleMessageField);
    });
    
    // Form validation
    form.addEventListener('submit', function(e) {
        const selectedAction = document.querySelector('input[name="action"]:checked').value;
        const fileInput = document.getElementById('file');
        
        if (!fileInput.files.length) {
            alert('Please select an image file');
            e.preventDefault();
            return;
        }
        
        if (selectedAction === 'encode') {
            const message = document.getElementById('message').value.trim();
            if (!message) {
                alert('Please enter a message to encode');
                e.preventDefault();
            }
        }
    });
});