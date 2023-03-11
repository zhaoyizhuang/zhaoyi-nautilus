import api from './api'

export default {
  async getStock (id, interval) {
    const response = await api.get(`stock/${id}`, {
      params: { interval }
    })
    return response.data
  }
}
