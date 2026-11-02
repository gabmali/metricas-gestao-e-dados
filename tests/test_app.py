from pathlib import Path
import pytest
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]

@pytest.mark.parametrize('file', ['app.py'] + [str(p.relative_to(ROOT)) for p in sorted((ROOT / 'pages').glob('*.py'))])
def test_pages_render(file):
    app = AppTest.from_file(str(ROOT / file), default_timeout=30).run(timeout=30)
    assert not app.exception
    branding = '\n'.join(item.value for item in app.sidebar.markdown)
    assert 'Métricas' in branding and 'Gestão e Dados' in branding
    assert 'DataVision' not in branding and 'ANALYTICS' not in branding

def test_empty_filter_and_clean_preview():
    app = AppTest.from_file(str(ROOT / 'app.py'), default_timeout=30).run()
    app.multiselect[0].set_value([]).run()
    assert not app.exception and app.info
    clean = AppTest.from_file(str(ROOT / 'pages/2_Limpeza.py'), default_timeout=30).run()
    next(b for b in clean.button if b.label == 'Gerar prévia de tratamento').click().run()
    assert not clean.exception
    assert 'clean_preview' in clean.session_state

def test_cleaning_can_activate_imported_copy():
    from src.data_generator import generate_sales
    import pandas as pd
    clean = AppTest.from_file(str(ROOT / 'pages/2_Limpeza.py'), default_timeout=30)
    data = generate_sales(8)
    clean.session_state['working_data'] = pd.concat([data, data.iloc[:1]], ignore_index=True)
    clean.session_state['raw_data'] = data.copy(deep=True)
    clean.run()
    next(b for b in clean.button if b.label == 'Gerar prévia de tratamento').click().run()
    next(b for b in clean.button if b.label == 'Validar e usar cópia tratada no dashboard').click().run()
    assert not clean.exception
    assert len(clean.session_state['sales']) == 8
    assert clean.session_state['working_data']['ID da venda'].is_unique
    assert clean.session_state['clean_preview'].isna().sum().sum() == 0
    assert any('8 vendas válidas' in c.value for c in clean.caption)
    assert any('0 células nulas' in c.value for c in clean.caption)
    assert any('Cópia validada e ativada' in s.value for s in clean.success)
    pd.testing.assert_frame_equal(clean.session_state['raw_data'], data)

def test_invalid_date_filter_and_reversed_dates():
    app = AppTest.from_file(str(ROOT / 'app.py'), default_timeout=30).run()
    app.text_input[0].set_value('31/02/2025').run()
    assert not app.exception and app.info
    app.text_input[0].set_value('31/12/2025').run()
    app.text_input[1].set_value('01/01/2024').run()
    assert not app.exception
    assert any('anterior ou igual' in i.value for i in app.info)

def test_metrics_are_responsive_cards_and_brazilian_numbers():
    app = AppTest.from_file(str(ROOT / 'app.py'), default_timeout=30).run()
    assert any('dv-metrics' in m.value and 'Receita total' in m.value for m in app.markdown)

def test_chart_dates_and_language():
    from src.charts import chart
    from src.data_generator import generate_sales
    fig = chart(generate_sales(30), 'Evolução mensal')
    assert fig.layout.separators == ',.'
    assert all('/' in label for label in fig.layout.xaxis.ticktext)
    assert 'Valor: R$' in fig.data[0].hovertemplate
