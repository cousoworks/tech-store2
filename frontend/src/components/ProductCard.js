import { Link } from 'react-router-dom';

const ProductCard = ({ product }) => {
  return (
    <div className="group relative bg-white border border-gray-200 rounded-lg shadow-sm overflow-hidden">
      <div className="aspect-h-1 aspect-w-1 w-full overflow-hidden bg-gray-200 xl:aspect-h-8 xl:aspect-w-7">
        {product.image_url ? (
          <img
            src={`http://localhost:8000/static/${product.image_url}`}
            alt={product.name}
            className="h-full w-full object-cover object-center group-hover:opacity-75"
          />
        ) : (
          <div className="h-full w-full flex items-center justify-center bg-gray-100 text-gray-500">
            No Image
          </div>
        )}
      </div>
      
      {product.is_used && (
        <span className="absolute top-2 right-2 inline-flex items-center rounded-md bg-yellow-50 px-2 py-1 text-xs font-medium text-yellow-800 ring-1 ring-inset ring-yellow-600/20">
          Used
        </span>
      )}
      
      <div className="p-4">
        <h3 className="text-sm font-medium text-gray-900">
          <Link to={`/products/${product.id}`}>
            <span aria-hidden="true" className="absolute inset-0" />
            {product.name}
          </Link>
        </h3>
        <p className="mt-1 text-sm text-gray-500 line-clamp-2">{product.description}</p>
        <div className="mt-2 flex items-center justify-between">
          <p className="text-lg font-medium text-gray-900">${product.price.toFixed(2)}</p>
          <p className="text-sm text-gray-500">{product.stock} in stock</p>
        </div>
      </div>
    </div>
  );
};

export default ProductCard;
