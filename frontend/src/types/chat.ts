export interface BuildComponent {
  category: string
  name: string
  price: number
  vendor: string
  url?: string
  image_url?: string
}

export interface AlternativeBuild {
  title: string
  description: string
  total_price: number
  components: BuildComponent[]
}

export interface ChatPlanResponse {
  plan_id: string
  generated_at: string
  total_price: number
  currency: string
  components: BuildComponent[]
  alternatives: AlternativeBuild[]
  summary: string
  notes?: string
}
