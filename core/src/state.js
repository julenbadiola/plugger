import create from 'zustand'

const useStore = create(set => ({
    initialized: false,
    accessToken: null,
}))

export default useStore