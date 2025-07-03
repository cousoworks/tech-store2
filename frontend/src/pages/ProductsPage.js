import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { productAPI, categoryAPI } from '../services/api';
import ProductCard from '../components/ProductCard';

export default function ProductsPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Filter and sort states
  const [searchQuery, setSearchQuery] = useState(searchParams.get('search') || '');
  const [minPrice, setMinPrice] = useState('');
  const [maxPrice, setMaxPrice] = useState('');
  const [sortBy, setSortBy] = useState('nombre');
  const [sortDesc, setSortDesc] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [isUsed, setIsUsed] = useState(null);
  const [categories, setCategories] = useState([]);

  // Fetch products when filters change
  useEffect(() => {
    const fetchProducts = async () => {
      setLoading(true);
      
      try {
        const params = {
          nombre: searchQuery || undefined,
        };
        
        const response = await productAPI.getProducts(params);
        // Adaptar la estructura de datos para que funcione con la interfaz
        const adaptedProducts = response.data.map(item => ({
          id: item.id,
          name: item.nombre,
          description: item.descripcion || '',
          price: item.precio,
          stock: item.cantidad,
          image_url: item.image_url,
          created_at: item.fecha_creacion
        }));
        setProducts(adaptedProducts);
        setError(null);
      } catch (err) {
        console.error('Error fetching products:', err);
        setError('Failed to load products');
      } finally {
        setLoading(false);
      }
    };

    // Update URL search params
    const newSearchParams = new URLSearchParams();
    if (searchQuery) newSearchParams.set('search', searchQuery);
    setSearchParams(newSearchParams);
    
    fetchProducts();
  }, [searchQuery, minPrice, maxPrice, sortBy, sortDesc, setSearchParams]);

  // Cargar categorías
  useEffect(() => {
    const fetchCategories = async () => {
      try {
        // Dado que no tenemos un endpoint de categorías en nuestra DB actual,
        // inicializamos con una lista vacía o podríamos crear categorías hardcodeadas
        // Cuando se implemente el endpoint de categorías, descomentar:
        // const response = await categoryAPI.getCategories();
        // setCategories(response.data);
        setCategories([]);
      } catch (err) {
        console.error('Error fetching categories:', err);
      }
    };
    
    fetchCategories();
  }, []);

  const handleFilter = (e) => {
    e.preventDefault();
    // The filter will be applied automatically by the useEffect dependency
  };

  const handleReset = () => {
    setSelectedCategory('');
    setSearchQuery('');
    setMinPrice('');
    setMaxPrice('');
    setSortBy('price');
    setSortDesc(true);
    setIsUsed(null);
  };

  return (
    <div className="bg-white">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row gap-6 py-6">
          {/* Filters */}
          <div className="md:w-1/4 lg:w-1/5">
            <form onSubmit={handleFilter} className="bg-white p-4 rounded-lg border border-gray-200 shadow-sm">
              <div className="space-y-4">
                <div>
                  <label htmlFor="search" className="block text-sm font-medium text-gray-700">
                    Search
                  </label>
                  <input
                    type="text"
                    id="search"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                  />
                </div>
                
                <div>
                  <label htmlFor="category" className="block text-sm font-medium text-gray-700">
                    Category
                  </label>
                  <select
                    id="category"
                    value={selectedCategory}
                    onChange={(e) => setSelectedCategory(e.target.value)}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                  >
                    <option value="">All Categories</option>
                    {categories.map((category) => (
                      <option key={category.id} value={category.id}>
                        {category.name}
                      </option>
                    ))}
                  </select>
                </div>
                
                <div>
                  <label htmlFor="minPrice" className="block text-sm font-medium text-gray-700">
                    Min Price
                  </label>
                  <input
                    type="number"
                    id="minPrice"
                    value={minPrice}
                    onChange={(e) => setMinPrice(e.target.value)}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                    min="0"
                    step="0.01"
                  />
                </div>
                
                <div>
                  <label htmlFor="maxPrice" className="block text-sm font-medium text-gray-700">
                    Max Price
                  </label>
                  <input
                    type="number"
                    id="maxPrice"
                    value={maxPrice}
                    onChange={(e) => setMaxPrice(e.target.value)}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                    min="0"
                    step="0.01"
                  />
                </div>
                
                <div>
                  <label htmlFor="condition" className="block text-sm font-medium text-gray-700">
                    Condition
                  </label>
                  <select
                    id="condition"
                    value={isUsed === null ? '' : isUsed ? 'used' : 'new'}
                    onChange={(e) => {
                      if (e.target.value === '') setIsUsed(null);
                      else setIsUsed(e.target.value === 'used');
                    }}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                  >
                    <option value="">All</option>
                    <option value="new">New</option>
                    <option value="used">Used</option>
                  </select>
                </div>
                
                <div>
                  <label htmlFor="sortBy" className="block text-sm font-medium text-gray-700">
                    Sort By
                  </label>
                  <select
                    id="sortBy"
                    value={`${sortBy}-${sortDesc ? 'desc' : 'asc'}`}
                    onChange={(e) => {
                      const [sort, direction] = e.target.value.split('-');
                      setSortBy(sort);
                      setSortDesc(direction === 'desc');
                    }}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                  >
                    <option value="price-asc">Price: Low to High</option>
                    <option value="price-desc">Price: High to Low</option>
                    <option value="created_at-desc">Newest First</option>
                    <option value="created_at-asc">Oldest First</option>
                  </select>
                </div>
                
                <div className="flex justify-between pt-2">
                  <button
                    type="submit"
                    className="inline-flex justify-center rounded-md bg-primary-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-primary-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-600"
                  >
                    Apply Filters
                  </button>
                  
                  <button
                    type="button"
                    onClick={handleReset}
                    className="rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
                  >
                    Reset
                  </button>
                </div>
              </div>
            </form>
          </div>

          {/* Product list */}
          <div className="md:w-3/4 lg:w-4/5">
            <h2 className="text-2xl font-bold tracking-tight text-gray-900 mb-6">Products</h2>
            
            {loading ? (
              <div className="flex justify-center items-center h-64">
                <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-600"></div>
              </div>
            ) : error ? (
              <div className="bg-red-50 border border-red-200 text-red-800 rounded-md p-4">
                {error}
              </div>
            ) : products.length === 0 ? (
              <div className="text-center py-10">
                <p className="text-gray-500">No products found matching your criteria.</p>
                <button
                  onClick={handleReset}
                  className="mt-4 inline-flex items-center rounded-md bg-primary-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-primary-500"
                >
                  Clear Filters
                </button>
              </div>
            ) : (
              <div className="grid grid-cols-1 gap-x-6 gap-y-10 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
                {products.map((product) => (
                  <ProductCard key={product.id} product={product} />
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
