class Api::AccountController < Api::ApiController

  def index
    success_response({'user': @current_user})
  end

end
