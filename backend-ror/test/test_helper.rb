ENV["RAILS_ENV"] ||= "test"
require_relative "../config/environment"
require "rails/test_help"

module ActiveSupport
  class TestCase
    # Run tests in parallel with specified workers
    parallelize(workers: :number_of_processors)

    # Setup all fixtures in test/fixtures/*.yml for all tests in alphabetical order.
    fixtures :all

    # Add more helper methods to be used by all tests here...
  end
end


module AuthenticatedTest
  def headers
    { 'Authorization': "Token #{@auth_token.token}" }
  end

  def setup_authentication
    @user = users(:one)
    @auth_token = AuthToken.create(user: @user)

  end
end
