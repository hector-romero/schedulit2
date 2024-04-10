ApiError = Struct.new(:type, :code, :detail, :attr)

API_ERRORS = {
  invalid_token: ApiError.new('authentication_error', 'authentication_failed', 'Invalid token.')
}

class Api::ApiController < ApplicationController
  include ActionController::HttpAuthentication::Token::ControllerMethods

  before_action :authenticate_user

  def success_response(data)
    render json: data, status: :ok
  end

  def error_response(data, status= :bad_request)
    render json: data, status: status
  end

  def authenticate_user
    authenticate_user_with_token || handle_bad_authentication
  end


  def handle_bad_authentication
    error_response(API_ERRORS[:invalid_token])
  end

  # sets @current_user if the request is authenticated
  def authenticate_user_with_token
    return true if @current_user  # avoid re-querying the DB
    authenticate_with_http_token do |token, options|
      auth_token =  AuthToken.get_by_token(token)
      unless auth_token and auth_token.user.is_active
        return false
      end
      # TODO Check user role, token expiration
      @current_user = auth_token.user
    end
  end
end
