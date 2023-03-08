import api from './api'

export default {
  async getStock (tickerId) {
    const response = await api.get(`stock/${tickerId}`)
    return response.data
  }
}
