let currentPage = 1;
const pageSize = 5;


async function loadProducts(page = 1) {
    try {
        const response = await axios.get(`/shop/products?current_page=${page}&number_prod=${pageSize}`);
        const products = response.data;

        const tableBody = document.querySelector('table tbody');
        tableBody.innerHTML = '';

        if (products.length === 0) {
            tableBody.innerHTML = `<tr><td colspan="4" class="text-center">Продукты не найдены</td></tr>`;
            return;
        }

        products.forEach(product => {
            const row = `
                <tr>
                    <td>${product.id}</td>
                    <td>${product.name}</td>
                    <td>${product.price}</td>
                    <td>${product.count}</td>
                </tr>
            `;
            tableBody.innerHTML += row;
        });

        currentPage = page;
    } catch (error) {
        alert('Ошибка загрузки продуктов: ' + (error.response?.data?.detail || error.message));
    }
}

function changePage(event, direction) {
    event.preventDefault();
    const newPage = currentPage + direction;
    if (newPage < 1) return;

    loadProducts(newPage);
}

function openAdminLoginForm(event) {
event.preventDefault();
const adminLoginModal = new bootstrap.Modal(document.getElementById('adminLoginModal'));
adminLoginModal.show();
}

async function submitAdminLoginForm() {
const username = document.getElementById('adminUsername').value;
const password = document.getElementById('adminPassword').value;

try {
    const response = await axios.post('/shop/admin/login', {
        admin_name: username,
        admin_password: password
    });

    if (response.data.access_token) {
        localStorage.setItem('adminToken', response.data.access_token);
        alert('Успешный вход! Токен сохранен.');
    } else {
        alert('Ошибка входа: Невалидный ответ от сервера.');
    }
} catch (error) {
    const errorMessage = error.response?.data?.detail || JSON.stringify(error.response?.data) || error.message;
    alert(`Ошибка входа: ${errorMessage}`);
}
}

function displayResults(data) {
const resultsContainer = document.getElementById('resultsContainer');
resultsContainer.style.display = 'block';
resultsContainer.innerHTML = `
    <p><strong>ID:</strong> ${data.id || 'N/A'}</p>
    <p><strong>Название:</strong> ${data.name || 'N/A'}</p>
    <p><strong>Цена:</strong> ${data.price || 'N/A'}</p>
    <p><strong>Количество:</strong> ${data.count || '0'}</p>
`;
}

document.getElementById('searchByNameForm').addEventListener('submit', async function(event) {
event.preventDefault();
const productName = document.getElementById('productName').value;

try {
    const response = await axios.get(`/shop/products/product/name/${productName}`);
    displayResults(response.data);
} catch (error) {
    alert('Ошибка поиска: ' + (error.response?.data?.detail || error.message));
}
});

document.getElementById('searchByIdForm').addEventListener('submit', async function(event) {
event.preventDefault();
const productId = document.getElementById('productId').value;

try {
    const response = await axios.get(`/shop/products/product/id/${productId}`);
    displayResults(response.data);
} catch (error) {
    alert('Ошибка поиска: ' + (error.response?.data?.detail || error.message));
}
});

document.addEventListener('DOMContentLoaded', () => {
    loadProducts(currentPage);
});
