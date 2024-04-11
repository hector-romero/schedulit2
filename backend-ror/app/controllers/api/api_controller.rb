require 'active_support/rescuable'
require "pg"

ApiError = Struct.new(:type, :code, :detail, :attr)

class Api::ApiController < ApplicationController
  include ActiveSupport::Rescuable
  include ActionController::HttpAuthentication::Token::ControllerMethods

  rescue_from Exception, with: :handle_unexpected_error
  rescue_from ActiveRecord::RecordNotUnique, with: :handle_duplicated_key_error
  rescue_from ActionController::ParameterMissing, with: :handle_missing_parameter_error
  rescue_from ActionDispatch::Http::Parameters::ParseError, with: :handle_invalid_request_error
  rescue_from ArgumentError, with: :handle_argument_error

  before_action :authenticate_user

  def handle_duplicated_key_error(error)
    message = 'Unexpected error'
    key = nil
    if error.message.include? 'DETAIL:'
      split_message = error.message.split('DETAIL:')[-1]
      key = split_message.tr("\n", '').gsub(/.*Key \((.*)\)=.*/, '\1')
      message = "#{key.humanize(keep_id_suffix: true)} is already in use"
    end
    error_response(ApiError.new('validation_error', 'unique', message, key))
  end

  def handle_argument_error(error)
    key = nil
    error_type = 'argument'
    if error.message.include?('is not a valid')
      key = error.message.gsub(/.*not a valid (.*)/, '\1')
      error_type = 'invalid_choice'
    end
    error_response(ApiError.new('validation_error', error_type, error.message, key))
  end

  def handle_missing_parameter_error(error)
    error_response(ApiError.new('validation_error', 'required', 'This field is required.', error.param))
  end

  def handle_unexpected_error(error)
    error_response(ApiError.new('unexpected_error', 'error', error.message))
  end

  def handle_invalid_request_error
    error_response(ApiError.new("invalid_request", "parse_error",  "JSON parse error"))
  end

  def handle_404_error
    error_response(ApiError.new('nout_found', 'not_found', 'Not found'), :not_found)
  end

  def handle_bad_authentication
    error_response(ApiError.new('authentication_error', 'authentication_failed', 'Invalid token.'),)
  end

  def validation_error(detail, code)
    error_response(ApiError.new('validation_error', code, detail))
  end

  def success_response(data)
    render json: data, status: :ok
  end

  def error_response(data, status= :bad_request)
    render json: data, status: status
  end

  def authenticate_user
    authenticate_user_with_token || handle_bad_authentication
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
      @auth_token = auth_token
    end
  end
end
