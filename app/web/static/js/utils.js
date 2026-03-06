export function openModal(modalId) {
    document.getElementById(modalId).style.display = 'block';
}

export function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

export function getErrorMessage(error) {
    if (typeof error.detail === 'string') {
        return error.detail;
    }
    if (Array.isArray(error.detail)) {
        return error.detail.join(', ');
    }
    return 'Error desconocido';
}