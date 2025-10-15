import type { ChatPlanResponse } from '../types/chat'

interface PlanPreviewProps {
  plan: ChatPlanResponse | null
}

export function PlanPreview({ plan }: PlanPreviewProps) {
  if (!plan) {
    return (
      <div className="panel panel-glass">
        <div className="panel-header">
          <h2>Plan Card</h2>
          <span className="panel-subtitle">Generated build plans will be shown here</span>
        </div>
        <div className="empty-state">
          <p>After you describe your needs and send, Builda will generate a primary and an alternative PC build plan.</p>
        </div>
      </div>
    )
  }

  return (
    <div className="panel panel-glass">
      <div className="panel-header">
        <h2>Primary Plan</h2>
        <div className="plan-header-meta">
          <span className="plan-total-pill">
            {plan.total_price.toLocaleString(undefined, { maximumFractionDigits: 2 })} {plan.currency}
          </span>
          <span className="plan-subtitle">Generated at {new Date(plan.generated_at).toLocaleTimeString()}</span>
        </div>
      </div>
      <div className="plan-summary">
        <p>{plan.summary}</p>
        {plan.notes && <p className="plan-notes">{plan.notes}</p>}
      </div>
      <div className="plan-components">
        {plan.components.map((component) => (
          <div key={`${component.category}-${component.name}`} className="plan-component">
            <div>
              <span className="plan-component-category">{component.category}</span>
              <p className="plan-component-name">{component.name}</p>
            </div>
            <div className="plan-component-meta">
              <span className="plan-component-vendor">{component.vendor}</span>
              <strong>{component.price.toLocaleString()} {plan.currency}</strong>
              {component.url && (
                <a className="plan-component-link" href={component.url} target="_blank" rel="noreferrer">
                  View
                </a>
              )}
            </div>
          </div>
        ))}
      </div>
      {plan.alternatives.length > 0 && (
        <div className="plan-alternatives">
          <h3>Alternative Plans</h3>
          {plan.alternatives.map((alternative) => (
            <div key={alternative.title} className="plan-alternative">
              <div className="plan-alternative-header">
                <div>
                  <h4>{alternative.title}</h4>
                  <p>{alternative.description}</p>
                </div>
                <span className="plan-alternative-total">
                  {alternative.total_price.toLocaleString()} {plan.currency}
                </span>
              </div>
              <ul>
                {alternative.components.map((component) => (
                  <li key={`${alternative.title}-${component.category}-${component.name}`}>
                    <span>{component.category}</span>
                    <p>{component.name}</p>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
