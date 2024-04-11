Rails.application.routes.draw do
  scope :api do
    scope :account, controller: :account do
      get '', action: 'index'
      post 'login', action: 'login'
      post 'register', action: 'register'
      post 'logout', action: 'logout'
      post 'logout/all', action: 'logout_all'
    end

    resources :users
    # Catch all for not defined paths
    match '*path', to: "api#handle_404_error", via: :all
  end
  # TODO remove
  resources :auth_tokens
  resources :shift_notes
  resources :shifts
  # Define your application routes per the DSL in https://guides.rubyonrails.org/routing.html

  # Reveal health status on /up that returns 200 if the app boots with no exceptions, otherwise 500.
  # Can be used by load balancers and uptime monitors to verify that the app is live.
  get "up" => "rails/health#show", as: :rails_health_check

  # Defines the root path route ("/")
  # root "posts#index"
end
