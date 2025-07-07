import { apiRequest, endpoints, normalizeApiResponse } from '../config/api';

// Auth Services
export const authService = {
  login: (email: string, password: string) =>
    apiRequest(endpoints.login, {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    }),
  
  logout: (refreshToken: string) =>
    apiRequest(endpoints.logout, {
      method: 'POST',
      body: JSON.stringify({ refresh: refreshToken }),
    }),
  
  getCurrentUser: () => apiRequest(endpoints.currentUser),
  
  getUsers: async () => {
    const response = await apiRequest(endpoints.users);
    return normalizeApiResponse(response);
  },
  
  createUser: (userData: any) => {
    // Créer FormData pour l'upload
    const formData = new FormData();
    
    // Ajouter les champs requis
    formData.append('email', userData.email);
    formData.append('nom', userData.nom);
    formData.append('prenom', userData.prenom);
    formData.append('password', userData.password);
    formData.append('role', userData.role);
    
    // Ajouter le magasin si fourni
    if (userData.magasin) {
      formData.append('magasin', userData.magasin);
    }
    
    // Ajouter l'image si fournie
    if (userData.image) {
      formData.append('image', userData.image);
    }
    
    return fetch(`http://localhost:8000/api/auth/users/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
      },
      body: formData,
    }).then(async response => {
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || errorData.message || `Erreur HTTP: ${response.status}`);
      }
      return response.json();
    });
  },
  
  updateUser: (id: string, userData: any) => {
    const formData = new FormData();
    
    // Ajouter les champs modifiables
    if (userData.nom) formData.append('nom', userData.nom);
    if (userData.prenom) formData.append('prenom', userData.prenom);
    if (userData.role) formData.append('role', userData.role);
    if (userData.magasin) formData.append('magasin', userData.magasin);
    if (userData.image) formData.append('image', userData.image);
    
    return fetch(`http://localhost:8000/api/auth/users/${id}/`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
      },
      body: formData,
    }).then(async response => {
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || errorData.message || `Erreur HTTP: ${response.status}`);
      }
      return response.json();
    });
  },
  
  deleteUser: (id: string) =>
    apiRequest(`${endpoints.users}${id}/`, { method: 'DELETE' }),
};

// Products Services
export const productsService = {
  getProducts: async () => {
    const response = await apiRequest(endpoints.products);
    return normalizeApiResponse(response);
  },
  
  createProduct: (productData: any) => {
    const formData = new FormData();
    
    formData.append('nom', productData.nom);
    formData.append('reference', productData.reference);
    formData.append('categorie', productData.categorie);
    formData.append('prix_unitaire', productData.prix_unitaire.toString());
    formData.append('seuil_alerte', productData.seuil_alerte.toString());
    
    if (productData.fournisseur) {
      formData.append('fournisseur', productData.fournisseur);
    }
    
    if (productData.image) {
      formData.append('image', productData.image);
    }
    
    return fetch(`http://localhost:8000/api/products/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
      },
      body: formData,
    }).then(async response => {
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || errorData.message || `Erreur HTTP: ${response.status}`);
      }
      return response.json();
    });
  },
  
  updateProduct: (id: string, productData: any) => {
    const formData = new FormData();
    
    formData.append('nom', productData.nom);
    formData.append('reference', productData.reference);
    formData.append('categorie', productData.categorie);
    formData.append('prix_unitaire', productData.prix_unitaire.toString());
    formData.append('seuil_alerte', productData.seuil_alerte.toString());
    
    if (productData.fournisseur) {
      formData.append('fournisseur', productData.fournisseur);
    }
    
    if (productData.image) {
      formData.append('image', productData.image);
    }
    
    return fetch(`http://localhost:8000/api/products/${id}/`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
      },
      body: formData,
    }).then(async response => {
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || errorData.message || `Erreur HTTP: ${response.status}`);
      }
      return response.json();
    });
  },
  
  deleteProduct: (id: string) =>
    apiRequest(`${endpoints.products}${id}/`, { method: 'DELETE' }),
};

// Stores Services
export const storesService = {
  getStores: async () => {
    const response = await apiRequest(endpoints.stores);
    return normalizeApiResponse(response);
  },
  
  createStore: (storeData: any) => {
    const formData = new FormData();
    
    formData.append('nom', storeData.nom);
    formData.append('adresse', storeData.adresse);
    formData.append('latitude', storeData.latitude.toString());
    formData.append('longitude', storeData.longitude.toString());
    
    if (storeData.image) {
      formData.append('image', storeData.image);
    }
    
    return fetch(`http://localhost:8000/api/stores/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
      },
      body: formData,
    }).then(async response => {
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || errorData.message || `Erreur HTTP: ${response.status}`);
      }
      return response.json();
    });
  },
  
  updateStore: (id: string, storeData: any) => {
    const formData = new FormData();
    
    formData.append('nom', storeData.nom);
    formData.append('adresse', storeData.adresse);
    formData.append('latitude', storeData.latitude.toString());
    formData.append('longitude', storeData.longitude.toString());
    
    if (storeData.image) {
      formData.append('image', storeData.image);
    }
    
    return fetch(`http://localhost:8000/api/stores/${id}/`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
      },
      body: formData,
    }).then(async response => {
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || errorData.message || `Erreur HTTP: ${response.status}`);
      }
      return response.json();
    });
  },
  
  deleteStore: (id: string) =>
    apiRequest(`${endpoints.stores}${id}/`, { method: 'DELETE' }),
};

// Suppliers Services
export const suppliersService = {
  getSuppliers: async () => {
    const response = await apiRequest(endpoints.suppliers);
    return normalizeApiResponse(response);
  },
  
  createSupplier: (supplierData: any) => {
    const formData = new FormData();
    
    formData.append('nom', supplierData.nom);
    formData.append('adresse', supplierData.adresse);
    formData.append('contact', supplierData.contact);
    
    if (supplierData.image) {
      formData.append('image', supplierData.image);
    }
    
    return fetch(`http://localhost:8000/api/suppliers/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
      },
      body: formData,
    }).then(async response => {
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || errorData.message || `Erreur HTTP: ${response.status}`);
      }
      return response.json();
    });
  },
  
  updateSupplier: (id: string, supplierData: any) => {
    const formData = new FormData();
    
    formData.append('nom', supplierData.nom);
    formData.append('adresse', supplierData.adresse);
    formData.append('contact', supplierData.contact);
    
    if (supplierData.image) {
      formData.append('image', supplierData.image);
    }
    
    return fetch(`http://localhost:8000/api/suppliers/${id}/`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
      },
      body: formData,
    }).then(async response => {
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || errorData.message || `Erreur HTTP: ${response.status}`);
      }
      return response.json();
    });
  },
  
  deleteSupplier: (id: string) =>
    apiRequest(`${endpoints.suppliers}${id}/`, { method: 'DELETE' }),
};

// Stock Services
export const stockService = {
  getStocks: async () => {
    const response = await apiRequest(endpoints.stocks);
    return normalizeApiResponse(response);
  },
  
  createStock: (stockData: any) =>
    apiRequest(endpoints.stocks, {
      method: 'POST',
      body: JSON.stringify(stockData),
    }),
  
  updateStock: (id: string, stockData: any) =>
    apiRequest(`${endpoints.stocks}${id}/`, {
      method: 'PUT',
      body: JSON.stringify(stockData),
    }),
  
  deleteStock: (id: string) =>
    apiRequest(`${endpoints.stocks}${id}/`, { method: 'DELETE' }),
  
  getMovements: async () => {
    const response = await apiRequest(endpoints.movements);
    return normalizeApiResponse(response);
  },
  
  createMovement: (movementData: any) =>
    apiRequest(endpoints.movements, {
      method: 'POST',
      body: JSON.stringify(movementData),
    }),
};

// Attendance Services
export const attendanceService = {
  getAttendance: async () => {
    const response = await apiRequest(endpoints.attendance);
    return normalizeApiResponse(response);
  },
  
  createAttendance: (attendanceData: any) =>
    apiRequest(endpoints.attendance, {
      method: 'POST',
      body: JSON.stringify(attendanceData),
    }),
  
  updateAttendance: (id: string, attendanceData: any) =>
    apiRequest(`${endpoints.attendance}${id}/`, {
      method: 'PUT',
      body: JSON.stringify(attendanceData),
    }),
  
  deleteAttendance: (id: string) =>
    apiRequest(`${endpoints.attendance}${id}/`, { method: 'DELETE' }),
};

// Messaging Services
export const messagingService = {
  getMessages: async () => {
    const response = await apiRequest(endpoints.messages);
    return normalizeApiResponse(response);
  },
  
  createMessage: (messageData: any) =>
    apiRequest(endpoints.messages, {
      method: 'POST',
      body: JSON.stringify(messageData),
    }),
  
  updateMessage: (id: string, messageData: any) =>
    apiRequest(`${endpoints.messages}${id}/`, {
      method: 'PUT',
      body: JSON.stringify(messageData),
    }),
  
  deleteMessage: (id: string) =>
    apiRequest(`${endpoints.messages}${id}/`, { method: 'DELETE' }),
};