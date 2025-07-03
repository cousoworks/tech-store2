import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { productAPI, categoryAPI } from '../services/api';
import ProductCard from '../components/ProductCard';

export default function HomePage() {
  const [popularProducts, setPopularProducts] = useState([]);
  const [newProducts, setNewProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        
        // Fetch data in parallel
        const [popularRes, newRes, categoriesRes] = await Promise.all([
          productAPI.getPopularProducts(),
          productAPI.getNewProducts(),
          categoryAPI.getCategories()
        ]);
        
        setPopularProducts(popularRes.data);
        setNewProducts(newRes.data);
        setCategories(categoriesRes.data);
      } catch (err) {
        console.error('Error fetching data:', err);
        setError('Failed to load products. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="bg-white">
      {/* Hero section */}
      <div className="relative bg-gray-900">
        <div className="mx-auto max-w-7xl lg:grid lg:grid-cols-12 lg:gap-x-8 lg:px-8">
          <div className="px-6 pt-10 pb-24 sm:pb-32 lg:col-span-7 lg:px-0 lg:pt-48 lg:pb-56 xl:col-span-6">
            <div className="mx-auto max-w-2xl lg:mx-0">
              <h1 className="mt-10 text-4xl font-bold tracking-tight text-white sm:text-6xl">
                Cutting-edge technology at your fingertips
              </h1>
              <p className="mt-6 text-lg leading-8 text-gray-300">
                Discover the latest in tech innovation. Buy new products or sell your used tech. 
                Join our community of tech enthusiasts today.
              </p>
              <div className="mt-10 flex items-center gap-x-6">
                <Link
                  to="/products"
                  className="rounded-md bg-primary-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-primary-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-600"
                >
                  Browse Products
                </Link>
                <Link to="/sell" className="text-sm font-semibold leading-6 text-white">
                  Sell Your Tech <span aria-hidden="true">→</span>
                </Link>
              </div>
            </div>
          </div>
          <div className="relative lg:col-span-5 lg:-mr-8 xl:absolute xl:inset-0 xl:left-1/2 xl:mr-0">
            <img
              className="aspect-[3/2] w-full bg-gray-50 object-cover lg:absolute lg:inset-0 lg:aspect-auto lg:h-full"
              src="https://images.unsplash.com/photo-1551434678-e076c223a692?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2070&q=80"
              alt=""
            />
          </div>
        </div>
      </div>

      {/* Categories section */}
      <div className="bg-gray-100">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="mx-auto max-w-2xl py-16 sm:py-24 lg:max-w-none lg:py-12">
            <h2 className="text-2xl font-bold text-gray-900">Browse Categories</h2>
            <div className="mt-6 space-y-12 lg:grid lg:grid-cols-3 lg:gap-x-6 lg:space-y-0">
              {categories.slice(0, 3).map((category) => (
                <div key={category.id} className="group relative">
                  <div className="relative h-80 w-full overflow-hidden rounded-lg bg-white sm:aspect-h-1 sm:aspect-w-2 lg:aspect-h-1 lg:aspect-w-1 group-hover:opacity-75 sm:h-64">
                    <div className="h-full w-full object-cover object-center flex items-center justify-center text-4xl text-gray-300 bg-gray-100">
                      {category.name.charAt(0)}
                    </div>
                  </div>
                  <h3 className="mt-6 text-sm text-gray-500">
                    <Link to={`/products?category=${category.id}`}>
                      <span className="absolute inset-0" />
                      {category.name}
                    </Link>
                  </h3>
                  <p className="text-base font-semibold text-gray-900">{category.description}</p>
                </div>
              ))}
            </div>
            <div className="mt-10 text-center">
              <Link
                to="/products"
                className="text-sm font-semibold leading-6 text-primary-600 hover:text-primary-500"
              >
                View all categories <span aria-hidden="true">→</span>
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Popular products section */}
      <div className="bg-white">
        <div className="mx-auto max-w-2xl px-4 py-16 sm:px-6 sm:py-24 lg:max-w-7xl lg:px-8">
          <h2 className="text-2xl font-bold tracking-tight text-gray-900">Popular Products</h2>
          
          {error ? (
            <div className="mt-6 text-center text-red-500">{error}</div>
          ) : (
            <div className="mt-6 grid grid-cols-1 gap-x-6 gap-y-10 sm:grid-cols-2 lg:grid-cols-4 xl:gap-x-8">
              {popularProducts.map((product) => (
                <ProductCard key={product.id} product={product} />
              ))}
            </div>
          )}
          
          <div className="mt-8 text-center">
            <Link
              to="/products"
              className="text-sm font-semibold leading-6 text-primary-600 hover:text-primary-500"
            >
              View all products <span aria-hidden="true">→</span>
            </Link>
          </div>
        </div>
      </div>
      
      {/* New arrivals section */}
      <div className="bg-gray-50">
        <div className="mx-auto max-w-2xl px-4 py-16 sm:px-6 sm:py-24 lg:max-w-7xl lg:px-8">
          <h2 className="text-2xl font-bold tracking-tight text-gray-900">New Arrivals</h2>
          
          {error ? (
            <div className="mt-6 text-center text-red-500">{error}</div>
          ) : (
            <div className="mt-6 grid grid-cols-1 gap-x-6 gap-y-10 sm:grid-cols-2 lg:grid-cols-4 xl:gap-x-8">
              {newProducts.map((product) => (
                <ProductCard key={product.id} product={product} />
              ))}
            </div>
          )}
          
          <div className="mt-8 text-center">
            <Link
              to="/products?sort=newest"
              className="text-sm font-semibold leading-6 text-primary-600 hover:text-primary-500"
            >
              View all new arrivals <span aria-hidden="true">→</span>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
