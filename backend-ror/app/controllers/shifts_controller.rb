class ShiftsController < ApiController
  before_action :set_shift, only: %i[ show update destroy ]

  # GET /shifts
  def index
    @shifts = Shift.where(employee_id: params['user_id'])
    render json: @shifts
  end

  # GET /shifts/1
  def show
    render json: @shift
  end

  # POST /shifts
  def create
    @shift = Shift.create!(new_shift_params)
    render json: @shift, status: :created, location: @shift
  end

  # PATCH/PUT /shifts/1
  def update
    @shift.update!(update_shift_params)
    render json: @shift
  end

  # DELETE /shifts/1
  def destroy
    @shift.destroy!
  end

  private
    # Use callbacks to share common setup or constraints between actions.
    def set_shift
      @shift = Shift.find(params[:id])
    end

    # Only allow a list of trusted parameters through.
    def new_shift_params
      params['employee_id'] = params['user_id']
      params.require([:employee_id, :start_time, :end_time])
      params.permit(:start_time, :end_time, :employee_id)
    end

    def update_shift_params
      params.permit(:start_time, :end_time, :status)
    end
end
