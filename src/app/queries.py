from pyspark.sql.functions import explode
from app import udfs


def get_counted_knowledge(extracted_recruit_df):
    '''
    Return a dataframe of 2 columns:
    Col1 (Knowledge): StringType, name of knowledge
    Col2 (count): IntegerType, number of appearances for each knowledge

    Parameters
    ----------
    extracted_recruit_df : orginal dataframe
    '''
    return extracted_recruit_df.withColumn("Knowledge", explode("Knowledges")).select("Knowledge").groupBy("Knowledge").count().orderBy("count",ascending=False)

def get_grouped_knowledge(knowledge_df, mapped_knowledge):
    '''
    Return a dataframe of 2 columns:
    Col1 (Category): StringType, name of category of knowledge
    Col2 (count): IntegerType, number of appearances for each category of knowledge

    Parameters
    ----------
    knowledge_df : dataframe of knowledges
    '''

    try:
        mapped_knowledge= mapped_knowledge.value['Knowledge']
    except:
        return None
    return knowledge_df.withColumn('Category', udfs.labeling_knowledge('Knowledge', mapped_knowledge))\
          .groupBy('Category').sum("count").filter("Category!='null'")
